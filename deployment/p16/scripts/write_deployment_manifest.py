from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="deployment/p16/deployment.json")
    parser.add_argument("--backend", choices=["lstm", "distilbert"], required=True)
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--model-version", required=True)
    parser.add_argument("--model-repo", required=True)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--model-label-map", default="{}")
    parser.add_argument("--dataset-repo", required=True)
    parser.add_argument("--dataset-revision", required=True)
    parser.add_argument("--code-revision", required=True)
    args = parser.parse_args()
    model_label_map = json.loads(args.model_label_map)
    if not isinstance(model_label_map, dict):
        parser.error("--model-label-map JSON object bo'lishi kerak")
    manifest = {
        "backend": args.backend,
        "model_name": args.model_name,
        "model_version": args.model_version,
        "model_repo": args.model_repo,
        "model_revision": args.model_revision,
        "model_label_map": model_label_map,
        "artifact_path": "artifacts/lstm-v1",
        "dataset_repo": args.dataset_repo,
        "dataset_revision": args.dataset_revision,
        "code_revision": args.code_revision,
        "low_confidence_threshold": 0.6,
        "alert_rate_threshold": 0.4,
    }
    Path(args.path).write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
