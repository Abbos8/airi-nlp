import json

import pytest

from capstone.modules.m13_bert_classifier import FineTunedClassifier


def test_normalizes_string_and_numeric_labels():
    assert FineTunedClassifier._normalize_labels(["salbiy", "ijobiy", 0, 1]) == [0, 1, 0, 1]
    with pytest.raises(ValueError, match="0 yoki 1"):
        FineTunedClassifier._normalize_labels([2])


def test_fit_validation_happens_before_model_download():
    classifier = FineTunedClassifier()
    with pytest.raises(ValueError, match="uzunligi teng"):
        classifier.fit(["yaxshi", "yomon"], ["ijobiy"])
    with pytest.raises(ValueError, match="kamida ikkita sinf"):
        classifier.fit(["yaxshi", "ajoyib"], ["ijobiy", "ijobiy"])


def test_predict_requires_fitted_model():
    with pytest.raises(RuntimeError, match=r"fit\(\) yoki load\(\)"):
        FineTunedClassifier().predict("yaxshi mahsulot")


def test_save_writes_huggingface_artifact_metadata(tmp_path):
    class FakeArtifact:
        def __init__(self, filename):
            self.filename = filename

        def save_pretrained(self, path):
            (path / self.filename).write_text("saved")

    classifier = FineTunedClassifier(max_length=96)
    classifier.model = FakeArtifact("model.safetensors")
    classifier.tokenizer = FakeArtifact("tokenizer.json")
    classifier.fitted = True
    classifier.save(tmp_path)

    metadata = json.loads((tmp_path / "capstone_metadata.json").read_text())
    assert metadata["max_length"] == 96
    assert metadata["base_model"] == FineTunedClassifier.DEFAULT_MODEL
    assert (tmp_path / "model.safetensors").exists()
    assert (tmp_path / "tokenizer.json").exists()
