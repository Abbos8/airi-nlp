from fastapi.testclient import TestClient

from p16_service.app import create_app
from p16_service.config import Settings


class FakeBackend:
    name = "test-lstm"
    version = "test-v1"

    def predict_proba(self, text: str) -> dict[str, float]:
        positive = 0.9 if "yaxshi" in text.lower() else 0.2
        return {"salbiy": 1 - positive, "ijobiy": positive}


def make_client() -> TestClient:
    settings = Settings(model_name="test-lstm", model_version="test-v1")
    return TestClient(create_app(backend=FakeBackend(), settings=settings))


def test_health_and_version():
    with make_client() as client:
        assert client.get("/health").json() == {
            "status": "ok",
            "model_name": "test-lstm",
            "model_version": "test-v1",
        }
        assert client.get("/version").json()["dataset_revision"]


def test_predict_validates_and_returns_lineage():
    with make_client() as client:
        response = client.post("/predict", json={"text": "Juda yaxshi mahsulot"})
        assert response.status_code == 200
        body = response.json()
        assert body["label"] == "ijobiy"
        assert body["confidence"] == 0.9
        assert body["model_version"] == "test-v1"
        assert client.post("/predict", json={"text": ""}).status_code == 422


def test_batch_updates_metrics():
    with make_client() as client:
        response = client.post(
            "/batch",
            json={"texts": ["yaxshi xizmat", "yetkazish juda yomon"]},
        )
        assert response.status_code == 200
        assert len(response.json()["predictions"]) == 2
        metrics = client.get("/metrics").json()
        assert metrics["request_count"] == 2
        assert metrics["label_counts"] == {"ijobiy": 1, "salbiy": 1}
