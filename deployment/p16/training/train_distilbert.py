from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

try:
    from .common import load_jsonl, sha256_file, stratified_split
except ImportError:
    from common import load_jsonl, sha256_file, stratified_split


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL = "distilbert-base-multilingual-cased"


def train_distilbert(
    data_path,
    output_dir,
    epochs=2,
    batch_size=16,
    model_name=DEFAULT_MODEL,
):
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from capstone.modules.m13_bert_classifier import FineTunedClassifier

    texts, labels = load_jsonl(data_path)
    train_x, train_y, test_x, test_y = stratified_split(texts, labels)
    classifier = FineTunedClassifier(max_length=128)
    started = time.perf_counter()
    classifier.fit(
        train_x,
        train_y,
        model_name=model_name,
        epochs=epochs,
        batch_size=batch_size,
        lr=2e-5,
    )
    training_seconds = time.perf_counter() - started
    metrics = classifier.evaluate(test_x, test_y)
    metrics.update(
        {
            "training_seconds": round(training_seconds, 3),
            "parameter_count": classifier.parameter_count,
            "dataset_revision": sha256_file(data_path),
            "train_examples": len(train_x),
            "test_examples": len(test_x),
        }
    )

    output_dir = Path(output_dir)
    classifier.save(output_dir)
    metrics["artifact_size_mb"] = round(
        sum(path.stat().st_size for path in output_dir.rglob("*") if path.is_file())
        / 1_000_000,
        3,
    )
    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", default="artifacts/distilbert-v1")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--model-name", default=DEFAULT_MODEL)
    args = parser.parse_args()
    metrics = train_distilbert(
        args.data,
        args.output,
        args.epochs,
        args.batch_size,
        args.model_name,
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
