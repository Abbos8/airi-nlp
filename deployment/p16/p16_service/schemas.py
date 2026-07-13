from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


InputText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2, max_length=2000),
]


class PredictRequest(BaseModel):
    text: InputText


class BatchRequest(BaseModel):
    texts: list[InputText] = Field(min_length=1, max_length=32)


class PredictionResponse(BaseModel):
    text: str
    label: str
    confidence: float = Field(ge=0.0, le=1.0)
    probabilities: dict[str, float]
    model_name: str
    model_version: str
    latency_ms: float = Field(ge=0.0)


class BatchResponse(BaseModel):
    predictions: list[PredictionResponse]
