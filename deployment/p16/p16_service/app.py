from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from .backends import PredictionBackend, build_backend
from .config import Settings
from .metrics import MetricsRegistry
from .schemas import BatchRequest, BatchResponse, PredictRequest, PredictionResponse


def create_app(
    backend: PredictionBackend | None = None,
    settings: Settings | None = None,
) -> FastAPI:
    settings = settings or Settings.from_manifest()
    metrics = MetricsRegistry(
        settings.low_confidence_threshold,
        settings.alert_rate_threshold,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.backend = backend or build_backend(settings)
        yield

    app = FastAPI(title="Uzbek Sentiment API", version="1.0.0", lifespan=lifespan)

    def predict_one(text: str, request: Request) -> PredictionResponse:
        started = time.perf_counter()
        try:
            probabilities = request.app.state.backend.predict_proba(text)
            label = max(probabilities, key=probabilities.get)
            confidence = probabilities[label]
            latency_ms = (time.perf_counter() - started) * 1000
            metrics.record_success(latency_ms, label, confidence)
            return PredictionResponse(
                text=text,
                label=label,
                confidence=confidence,
                probabilities=probabilities,
                model_name=request.app.state.backend.name,
                model_version=request.app.state.backend.version,
                latency_ms=latency_ms,
            )
        except Exception as error:
            metrics.record_error()
            raise HTTPException(status_code=500, detail="Model inference failed") from error

    @app.get("/health")
    def health(request: Request):
        loaded = request.app.state.backend
        return {"status": "okay", "model_name": loaded.name, "model_version": loaded.version}

    @app.get("/version")
    def version():
        return settings.public_metadata()

    @app.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictRequest, request: Request):
        return predict_one(payload.text, request)

    @app.post("/batch", response_model=BatchResponse)
    def batch(payload: BatchRequest, request: Request):
        return BatchResponse(predictions=[predict_one(text, request) for text in payload.texts])

    @app.get("/metrics")
    def service_metrics():
        return metrics.snapshot()

    return app


app = create_app()
