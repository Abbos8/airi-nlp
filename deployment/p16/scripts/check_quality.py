from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics")
    parser.add_argument("--min-f1", type=float, default=0.70)
    parser.add_argument("--max-latency-ms", type=float, default=100.0)
    args = parser.parse_args()
    metrics = json.loads(Path(args.metrics).read_text())
    failures = []
    if metrics["f1"] < args.min_f1:
        failures.append(f"f1={metrics['f1']} < {args.min_f1}")
    if metrics["inference_time"] > args.max_latency_ms:
        failures.append(
            f"inference_time={metrics['inference_time']} > {args.max_latency_ms} ms"
        )
    if failures:
        raise SystemExit("Quality gate failed: " + "; ".join(failures))
    print("Quality gate passed:", json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
