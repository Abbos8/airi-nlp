from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from capstone.modules.m08_gru_lstm_classifier import (  # noqa: E402
    GRULSTMClassifier,
    LSTMClassifier,
    _TorchSequenceNet,
)


TEXTS = [
    "juda yaxshi mahsulot",
    "ajoyib tez xizmat",
    "sifatli va yaxshi",
    "mamnun bo'ldim",
    "sifatsiz yomon mahsulot",
    "juda yomon xizmat",
    "umuman ishlamadi",
    "tavsiya qilmayman",
]
LABELS = ["ijobiy"] * 4 + ["salbiy"] * 4


@pytest.mark.parametrize("architecture", ["lstm", "gru"])
def test_padding_does_not_change_logits(architecture):
    torch.manual_seed(42)
    model = _TorchSequenceNet(20, 8, 12, 1, 2, architecture).eval()
    with torch.inference_mode():
        short = model(torch.tensor([[1, 2, 3]]), torch.tensor([3]))
        padded = model(torch.tensor([[1, 2, 3, 0, 0, 0]]), torch.tensor([3]))
    assert torch.allclose(short, padded)


def test_fit_validates_inputs():
    model = LSTMClassifier()
    with pytest.raises(ValueError, match="uzunligi teng"):
        model.fit(["yaxshi", "yomon"], ["ijobiy"])
    with pytest.raises(ValueError, match="kamida ikkita sinf"):
        model.fit(["yaxshi", "ajoyib"], ["ijobiy", "ijobiy"])


def test_save_load_round_trip(tmp_path: Path):
    model = LSTMClassifier(embed_dim=8)
    model.fit(TEXTS, LABELS, epochs=2, hidden_size=12, num_layers=1)
    before = model.predict_proba("juda yaxshi")
    artifact = tmp_path / "lstm.pkl"
    model.save(artifact)

    restored = LSTMClassifier()
    restored.load(artifact)
    after = restored.predict_proba("juda yaxshi")
    assert before == pytest.approx(after)


def test_compare_report_uses_validation_metrics():
    model = GRULSTMClassifier(embed_dim=8)
    model.fit(TEXTS, LABELS, epochs=1, hidden_size=8, num_layers=1)
    report = model.compare_report()
    assert set(report) == {"lstm", "gru"}
    assert all(
        {"f1", "accuracy", "val_loss", "inference_time"} <= set(metrics)
        for metrics in report.values()
    )
