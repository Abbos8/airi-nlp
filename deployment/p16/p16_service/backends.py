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


def build_backend(settings: Settings) -> PredictionBackend:
    if settings.backend != "lstm":
        raise ValueError(f"Noma'lum backend: {settings.backend}")
    return LSTMBackend(settings.artifact_path, settings)
