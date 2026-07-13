from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from .config import Settings
from .preprocessing import preprocess


class PredictionBackend(Protocol):
    name: str
    version: str

    def predict_proba(self, text: str) -> dict[str, float]: ...


def _project_probabilities(
    raw_labels: list[str],
    probabilities: list[float],
    label_map: dict[str, str | None],
) -> dict[str, float]:
    """Map external labels to the service contract and renormalize kept classes."""
    projected: dict[str, float] = {}
    for raw_label, probability in zip(raw_labels, probabilities):
        target_label = label_map.get(raw_label, raw_label)
        if target_label is None:
            continue
        projected[target_label] = projected.get(target_label, 0.0) + float(probability)

    total = sum(projected.values())
    if not projected or total <= 0:
        raise ValueError("Model label mapping barcha chiqish sinflarini olib tashladi.")
    return {label: probability / total for label, probability in projected.items()}


class _LSTMNetwork:
    """Build the same PyTorch graph used by the Day 9 capstone class."""

    @staticmethod
    def build(config: dict):
        import torch.nn as nn

        class Network(nn.Module):
            def __init__(self):
                super().__init__()
                self.embedding = nn.Embedding(
                    config["vocab_size"], config["embed_dim"], padding_idx=0
                )
                self.recurrent = nn.LSTM(
                    config["embed_dim"],
                    config["hidden_size"],
                    num_layers=config["num_layers"],
                    batch_first=True,
                )
                self.output = nn.Linear(config["hidden_size"], len(config["labels"]))

            def forward(self, token_ids):
                embedded = self.embedding(token_ids)
                _, (hidden, _) = self.recurrent(embedded)
                return self.output(hidden[-1])

        return Network()


class LSTMBackend:
    def __init__(self, artifact_dir: str | Path, settings: Settings):
        import torch

        artifact_dir = Path(artifact_dir)
        config = json.loads((artifact_dir / "config.json").read_text())
        self.vocab = json.loads((artifact_dir / "vocab.json").read_text())
        self.labels = config["labels"]
        self.model = _LSTMNetwork.build(config)
        state = torch.load(artifact_dir / "model.pt", map_location="cpu", weights_only=True)
        self.model.load_state_dict(state)
        self.model.eval()
        self.name = settings.model_name
        self.version = settings.model_version

    def predict_proba(self, text: str) -> dict[str, float]:
        import torch

        token_ids = [self.vocab[token] for token in preprocess(text) if token in self.vocab]
        inputs = torch.tensor([token_ids or [0]], dtype=torch.long)
        with torch.inference_mode():
            probabilities = torch.softmax(self.model(inputs)[0], dim=-1).tolist()
        return dict(zip(self.labels, map(float, probabilities)))


class DistilBERTBackend:
    def __init__(self, settings: Settings):
        if not settings.model_repo:
            raise ValueError("DistilBERT uchun MODEL_REPO ko'rsatilishi kerak.")

        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        revision = settings.model_revision or "main"
        self.tokenizer = AutoTokenizer.from_pretrained(settings.model_repo, revision=revision)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            settings.model_repo, revision=revision
        )
        self.model.eval()
        configured_labels = self.model.config.id2label or {}
        num_labels = int(self.model.config.num_labels)
        self.raw_labels = [
            configured_labels.get(i, configured_labels.get(str(i), str(i)))
            for i in range(num_labels)
        ]
        self.label_map = settings.model_label_map or {}
        self.name = settings.model_name
        self.version = settings.model_version

    def predict_proba(self, text: str) -> dict[str, float]:
        import torch

        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
        with torch.inference_mode():
            logits = self.model(**inputs).logits[0]
            probabilities = torch.softmax(logits, dim=-1).tolist()
        return _project_probabilities(self.raw_labels, probabilities, self.label_map)


def build_backend(settings: Settings) -> PredictionBackend:
    if settings.backend == "distilbert":
        return DistilBERTBackend(settings)
    if settings.backend != "lstm":
        raise ValueError(f"Noma'lum backend: {settings.backend}")

    if settings.model_repo:
        from huggingface_hub import snapshot_download

        artifact_dir = snapshot_download(
            repo_id=settings.model_repo,
            revision=settings.model_revision or "main",
        )
    else:
        artifact_dir = settings.artifact_path
    return LSTMBackend(artifact_dir, settings)
