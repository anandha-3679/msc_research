"""
Tests for src/doda/clinical_broker.py.

These exist specifically to catch, automatically, the class of bug found in
the original diabetes prototype: an incomplete clinical weight dictionary
that silently defaults missing features to a neutral weight, which quietly
changes which features end up in the Top-K feature space. Run with:

    pytest tests/
"""

from pathlib import Path

import pandas as pd
import pytest
import yaml

from doda.clinical_broker import ClinicalKnowledgeBroker, apply_clinical_weights

CONFIG_DIR = Path(__file__).resolve().parents[1] / "config" / "clinical_weights"

# Feature lists per dataset — kept here (not imported from a live DataFrame)
# so these tests don't require the raw data files to be present locally.
DATASET_FEATURES = {
    "diabetes": [
        "HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke",
        "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
        "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth",
        "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income",
    ],
}


@pytest.mark.parametrize("disease", list(DATASET_FEATURES.keys()))
def test_every_dataset_feature_has_a_weight(disease):
    """The core regression test for the original bug: fails loudly if any
    feature the dataset actually has is missing from the YAML file, instead
    of letting it silently default to a neutral weight downstream.
    """
    weights_path = CONFIG_DIR / f"{disease}.yaml"
    broker = ClinicalKnowledgeBroker(weights_path)
    broker.validate_against(DATASET_FEATURES[disease])  # raises if incomplete


@pytest.mark.parametrize("yaml_file", sorted(CONFIG_DIR.glob("*.yaml")))
def test_weights_are_in_valid_range(yaml_file):
    """Weights should be within [0, 1] except for deliberate, documented
    exceptions (none currently) — catches accidental values like the
    prototype's undocumented Stroke=2.5 override.
    """
    with open(yaml_file) as f:
        weights = yaml.safe_load(f)

    for feature, weight in weights.items():
        assert 0.0 <= weight <= 1.0, (
            f"{yaml_file.name}: '{feature}' has weight {weight}, outside "
            "[0, 1]. If this is intentional, document why in a comment "
            "directly above the entry."
        )


def test_get_weight_raises_on_unknown_feature(tmp_path):
    """get_weight() must raise, not silently default, for a feature that
    isn't in the YAML file — this is the specific behavior that differs
    from the original prototype's fillna(1.0) approach.
    """
    weights_file = tmp_path / "toy.yaml"
    weights_file.write_text("FeatureA: 0.5\nFeatureB: 0.8\n")
    broker = ClinicalKnowledgeBroker(weights_file)

    assert broker.get_weight("FeatureA") == 0.5
    with pytest.raises(KeyError):
        broker.get_weight("FeatureC_not_defined")


def test_apply_clinical_weights_reweights_correctly(tmp_path):
    """End-to-end check of the Hadamard re-weighting step (Phase 3)."""
    weights_file = tmp_path / "toy.yaml"
    weights_file.write_text("FeatureA: 1.0\nFeatureB: 0.2\n")
    broker = ClinicalKnowledgeBroker(weights_file)

    statistical_scores = pd.DataFrame({
        "Feature": ["FeatureA", "FeatureB"],
        "Final_Score": [0.5, 0.6],
    })

    result = apply_clinical_weights(statistical_scores, broker)

    # FeatureA: 0.5 * 1.0 = 0.5 ; FeatureB: 0.6 * 0.2 = 0.12
    # So FeatureA should now rank ABOVE FeatureB despite the lower raw score.
    assert result.iloc[0]["Feature"] == "FeatureA"
    assert result.iloc[0]["Clinical_Adjusted_Score"] == pytest.approx(0.5)
    assert result.iloc[1]["Clinical_Adjusted_Score"] == pytest.approx(0.12)
