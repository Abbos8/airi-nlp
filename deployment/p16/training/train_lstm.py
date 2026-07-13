from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import torch

try:
    from .common import LABEL_NAMES, load_jsonl, sha256_file, stratified_split
except ImportError:
    from common import LABEL_NAMES, load_jsonl, sha256_file, stratified_split


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA = REPO_ROOT / "practices/d14_checkpoints/uz_sentiment_mini.jsonl"


def current_code_revision() -> str:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=REPO_ROOT, text=True
        ).strip()
        return f"{sha}-dirty" if dirty else sha
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def resolve_dataset(data_path, dataset_repo=None, dataset_revision=None):
    if not dataset_repo:
        return Path(data_path), f"course-local:{Path(data_path).name}"
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(
        repo_id=dataset_repo,
        repo_type="dataset",
        filename="uz_sentiment_mini.jsonl",
        revision=dataset_revision,
    )
    return Path(path), dataset_repo


def export_capstone_lstm(model, output_dir: Path, metadata: dict) -> dict:
    """Convert the Day 9 capstone object into an explicit serving artifact."""
    output_dir.mkdir(parents=True, exist_ok=True)
    config = {
        "architecture": "lstm",
        "vocab_size": len(model._w2i) + 1,
        "embed_dim": model._dim,
        "hidden_size": model._config.hidden_size,
        "num_layers": model._config.num_layers,
        "labels": model._labels,
        "preprocessing_version": "m01-v1",
        **metadata,
    }
    torch.save(model._model.state_dict(), output_dir / "model.pt")
    (output_dir / "config.json").write_text(json.dumps(config, indent=2))
    (output_dir / "vocab.json").write_text(json.dumps(model._w2i, indent=2))
    return config


def train_lstm(
    data_path: str | Path,
    output_dir: str | Path,
    epochs: int = 8,
    hidden_size: int = 64,
    model_version: str = "v1",
    dataset_repo: str | None = None,
    dataset_revision: str | None = None,
) -> dict:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from capstone.modules.m08_gru_lstm_classifier import LSTMClassifier

    data_path, dataset_source = resolve_dataset(data_path, dataset_repo, dataset_revision)
    texts, numeric_labels = load_jsonl(data_path)
    train_x, train_y, test_x, test_y = stratified_split(texts, numeric_labels)
    train_labels = [LABEL_NAMES[label] for label in train_y]
    test_labels = [LABEL_NAMES[label] for label in test_y]

    started = time.perf_counter()
    model = LSTMClassifier(embed_dim=32)
    model.fit(
        train_x,
        train_labels,
        epochs=epochs,
        hidden_size=hidden_size,
        num_layers=1,
        lr=3e-3,
    )
    training_seconds = time.perf_counter() - started
    metrics = model.evaluate(test_x, test_labels)
    metrics.update(
        {
            "training_seconds": round(training_seconds, 3),
            "parameter_count": sum(p.numel() for p in model._model.parameters()),
            "train_examples": len(train_x),
            "test_examples": len(test_x),
        }
    )

    output_dir = Path(output_dir)
    metadata = {
        "model_name": "uzbek-sentiment-lstm",
        "model_version": model_version,
        "dataset_repo": dataset_source,
        "dataset_revision": dataset_revision or sha256_file(data_path),
        "code_revision": current_code_revision(),
    }
    export_capstone_lstm(model, output_dir, metadata)
    metrics["artifact_size_mb"] = round(
        sum(path.stat().st_size for path in output_dir.iterdir()) / 1_000_000, 3
    )
    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return {"metrics": metrics, "metadata": metadata, "artifact_dir": str(output_dir)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--output", default="deployment/p16/artifacts/lstm-v1")
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--hidden-size", type=int, default=64)
    parser.add_argument("--model-version", default="v1")
    parser.add_argument("--dataset-repo")
    parser.add_argument("--dataset-revision")
    args = parser.parse_args()
    result = train_lstm(
        args.data,
        args.output,
        args.epochs,
        args.hidden_size,
        args.model_version,
        args.dataset_repo,
        args.dataset_revision,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
