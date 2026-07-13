from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


LABEL_NAMES = {0: "salbiy", 1: "ijobiy"}


def load_jsonl(path: str | Path) -> tuple[list[str], list[int]]:
    records = [json.loads(line) for line in Path(path).read_text().splitlines() if line]
    return [row["text"] for row in records], [int(row["label"]) for row in records]


def stratified_split(
    texts: list[str], labels: list[int], test_ratio: float = 0.2, seed: int = 42
):
    rng = random.Random(seed)
    train_indices: list[int] = []
    test_indices: list[int] = []
    for label in sorted(set(labels)):
        indices = [index for index, value in enumerate(labels) if value == label]
        rng.shuffle(indices)
        test_count = max(1, round(len(indices) * test_ratio))
        test_indices.extend(indices[:test_count])
        train_indices.extend(indices[test_count:])
    rng.shuffle(train_indices)
    rng.shuffle(test_indices)
    select = lambda values, indices: [values[index] for index in indices]
    return (
        select(texts, train_indices),
        select(labels, train_indices),
        select(texts, test_indices),
        select(labels, test_indices),
    )


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def classification_metrics(y_true: list[int], y_pred: list[int]) -> dict[str, float]:
    accuracy = sum(a == b for a, b in zip(y_true, y_pred)) / max(len(y_true), 1)
    f1_scores = []
    for label in sorted(set(y_true) | set(y_pred)):
        tp = sum(a == label and b == label for a, b in zip(y_true, y_pred))
        fp = sum(a != label and b == label for a, b in zip(y_true, y_pred))
        fn = sum(a == label and b != label for a, b in zip(y_true, y_pred))
        precision = tp / max(tp + fp, 1)
        recall = tp / max(tp + fn, 1)
        f1_scores.append(2 * precision * recall / max(precision + recall, 1e-12))
    return {"accuracy": round(accuracy, 4), "f1": round(sum(f1_scores) / len(f1_scores), 4)}
