from __future__ import annotations

from collections import Counter, deque
import math
from threading import Lock


class MetricsRegistry:
    def __init__(self, low_confidence_threshold: float, alert_rate_threshold: float):
        self.low_confidence_threshold = low_confidence_threshold
        self.alert_rate_threshold = alert_rate_threshold
        self._latencies: deque[float] = deque(maxlen=1000)
        self._labels: Counter[str] = Counter()
        self._requests = 0
        self._errors = 0
        self._low_confidence = 0
        self._lock = Lock()

    def record_success(self, latency_ms: float, label: str, confidence: float) -> None:
        with self._lock:
            self._requests += 1
            self._latencies.append(latency_ms)
            self._labels[label] += 1
            self._low_confidence += confidence < self.low_confidence_threshold

    def record_error(self) -> None:
        with self._lock:
            self._requests += 1
            self._errors += 1

    def snapshot(self) -> dict:
        with self._lock:
            ordered = sorted(self._latencies)
            average = sum(ordered) / len(ordered) if ordered else 0.0
            p95_index = max(0, math.ceil(0.95 * len(ordered)) - 1)
            p95 = ordered[p95_index] if ordered else 0.0
            successful = max(self._requests - self._errors, 1)
            low_rate = self._low_confidence / successful
            return {
                "request_count": self._requests,
                "error_count": self._errors,
                "average_latency_ms": round(average, 3),
                "p95_latency_ms": round(p95, 3),
                "low_confidence_rate": round(low_rate, 3),
                "quality_alert": self._requests >= 5 and low_rate >= self.alert_rate_threshold,
                "label_counts": dict(self._labels),
            }
