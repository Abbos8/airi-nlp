from pathlib import Path

import pytest

from p16_service.backends import LSTMBackend
from p16_service.config import Settings


ARTIFACT_DIR = Path(__file__).resolve().parents[1] / "artifacts/lstm-v1"


def test_bundled_lstm_loads_and_predicts_probabilities():
    backend = LSTMBackend(ARTIFACT_DIR, Settings())

    probabilities = backend.predict_proba("Mahsulot sifati juda yaxshi")

    assert set(probabilities) == {"ijobiy", "salbiy"}
    assert sum(probabilities.values()) == pytest.approx(1.0)
    assert all(0.0 <= value <= 1.0 for value in probabilities.values())
