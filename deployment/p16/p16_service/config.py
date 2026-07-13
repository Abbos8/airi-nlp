from __future__ import annotations

import json
import os
from dataclasses import dataclass, replace
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    backend: str = "lstm"
    model_name: str = "uzbek-sentiment-lstm"
    model_version: str = "bundled-v1"
    model_repo: str | None = None
    model_revision: str | None = None
    model_label_map: dict[str, str | None] | None = None
    artifact_path: str = "artifacts/lstm-v1"
    dataset_repo: str = "course-local:uz_sentiment_mini.jsonl"
    dataset_revision: str = "local-course-snapshot"
    code_revision: str = "working-tree"
    low_confidence_threshold: float = 0.60
    alert_rate_threshold: float = 0.40

    @classmethod
    def from_manifest(cls, path: str | Path = "deployment.json") -> "Settings":
        manifest_path = Path(path)
        values = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        settings = cls(**values)
        overrides = {
            "backend": os.getenv("MODEL_BACKEND"),
            "model_name": os.getenv("MODEL_NAME"),
            "model_version": os.getenv("MODEL_VERSION"),
            "model_repo": os.getenv("MODEL_REPO"),
            "model_revision": os.getenv("MODEL_REVISION"),
            "artifact_path": os.getenv("MODEL_ARTIFACT_PATH"),
            "code_revision": os.getenv("CODE_REVISION"),
        }
        raw_label_map = os.getenv("MODEL_LABEL_MAP")
        if raw_label_map:
            label_map = json.loads(raw_label_map)
            if not isinstance(label_map, dict):
                raise ValueError("MODEL_LABEL_MAP JSON object bo'lishi kerak.")
            overrides["model_label_map"] = label_map
        return replace(settings, **{key: value for key, value in overrides.items() if value})

    def public_metadata(self) -> dict[str, object]:
        return {
            "backend": self.backend,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "model_repo": self.model_repo,
            "model_revision": self.model_revision,
            "model_label_map": self.model_label_map,
            "dataset_repo": self.dataset_repo,
            "dataset_revision": self.dataset_revision,
            "code_revision": self.code_revision,
        }
