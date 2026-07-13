from p16_service.metrics import MetricsRegistry


def test_quality_alert_requires_enough_requests():
    metrics = MetricsRegistry(low_confidence_threshold=0.6, alert_rate_threshold=0.4)
    for _ in range(4):
        metrics.record_success(10.0, "ijobiy", 0.5)
    assert metrics.snapshot()["quality_alert"] is False

    metrics.record_success(20.0, "salbiy", 0.5)
    snapshot = metrics.snapshot()
    assert snapshot["quality_alert"] is True
    assert snapshot["p95_latency_ms"] == 20.0
