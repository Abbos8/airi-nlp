import pytest

from p16_service.backends import _project_probabilities


def test_external_three_class_model_projects_to_binary_contract():
    result = _project_probabilities(
        ["LABEL_0", "LABEL_1", "LABEL_2"],
        [0.2, 0.3, 0.5],
        {"LABEL_0": "salbiy", "LABEL_1": "ijobiy", "LABEL_2": None},
    )

    assert result == pytest.approx({"salbiy": 0.4, "ijobiy": 0.6})
    assert sum(result.values()) == pytest.approx(1.0)


def test_projection_rejects_mapping_that_drops_every_class():
    with pytest.raises(ValueError, match="barcha chiqish sinflarini"):
        _project_probabilities(["neutral"], [1.0], {"neutral": None})
