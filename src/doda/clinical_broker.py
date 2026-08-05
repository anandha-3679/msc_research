"""
The DODA Clinical Knowledge Layer.

This module is deliberately the ONLY place clinical weights are defined or
applied. In the original prototype notebook, two separate in-code dictionaries
existed for the same disease (one in a ClinicalKnowledgeBroker class, one as a
later "# Clinical correction" override), and the override silently fell back
to a neutral weight of 1.0 for any feature it didn't mention — which is what
let an unrelated feature (HvyAlcoholConsump) outrank a feature the override was
specifically trying to boost (Stroke). See docs/known_issues.md, item 1.

The fix here is structural, not just a corrected number:
  1. Weights live in config/clinical_weights/<disease>.yaml — one file, one
     source of truth, no in-code dictionaries.
  2. get_weight() raises an error (not a silent default) if a feature is
     missing from the YAML file, so an incomplete dictionary fails loudly
     at run time instead of quietly reshaping the results.
"""

from pathlib import Path
from typing import Union

import pandas as pd
import yaml


class ClinicalKnowledgeBroker:
    """Loads a disease's clinical weight dictionary and exposes lookups.

    Parameters
    ----------
    weights_path : str or Path
        Path to a YAML file mapping feature name -> clinical weight (float).
        See config/clinical_weights/ for the per-disease files.
    """

    def __init__(self, weights_path: Union[str, Path]):
        self.weights_path = Path(weights_path)
        with open(self.weights_path, "r") as f:
            self.weights = yaml.safe_load(f)

        if not isinstance(self.weights, dict) or not self.weights:
            raise ValueError(
                f"{self.weights_path} did not load as a non-empty dictionary. "
                "Check the YAML file is well-formed."
            )

    def get_weight(self, feature: str) -> float:
        """Return the clinical weight for a feature.

        Deliberately raises KeyError rather than defaulting to a neutral
        weight — an incomplete clinical_weights YAML file should fail loudly,
        not silently inflate an unlisted feature's importance.
        """
        if feature not in self.weights:
            raise KeyError(
                f"'{feature}' is not defined in {self.weights_path}. "
                "Every feature in the dataset must have an explicit clinical "
                "weight — add it rather than relying on a default."
            )
        return float(self.weights[feature])

    def validate_against(self, feature_names: list[str]) -> None:
        """Raise an error if any dataset feature is missing a weight, or if
        the YAML file defines weights for features that don't exist in the
        dataset (a likely typo). Call this once per notebook, right after
        loading the dataset, before running Phase 3.
        """
        dataset_features = set(feature_names)
        yaml_features = set(self.weights.keys())

        missing = dataset_features - yaml_features
        extra = yaml_features - dataset_features

        if missing:
            raise KeyError(
                f"{self.weights_path} is missing weights for: {sorted(missing)}"
            )
        if extra:
            raise KeyError(
                f"{self.weights_path} defines weights for features not in the "
                f"dataset (possible typo): {sorted(extra)}"
            )


def apply_clinical_weights(
    statistical_scores: pd.DataFrame,
    broker: ClinicalKnowledgeBroker,
    feature_col: str = "Feature",
    score_col: str = "Final_Score",
) -> pd.DataFrame:
    """Apply the Hadamard (element-wise) re-weighting step: Phase 3 of DODA.

    Parameters
    ----------
    statistical_scores : DataFrame with columns [feature_col, score_col]
        The consensus statistical ranking produced in Phase 2.
    broker : ClinicalKnowledgeBroker
        Already loaded with the disease's clinical weight dictionary.

    Returns
    -------
    DataFrame with an added Clinical_Weight and Clinical_Adjusted_Score column,
    sorted by Clinical_Adjusted_Score descending.
    """
    df = statistical_scores.copy()
    df["Clinical_Weight"] = df[feature_col].apply(broker.get_weight)
    df["Clinical_Adjusted_Score"] = df[score_col] * df["Clinical_Weight"]
    return df.sort_values("Clinical_Adjusted_Score", ascending=False).reset_index(drop=True)
