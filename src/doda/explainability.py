"""
Phase 6 explainability axis: SHAP comparison between baseline and
DODA-adjusted feature spaces.

This module is new — the diabetes prototype notebook implemented three of
the proposal's four evaluation axes (predictive performance, clinical
relevance, feature stability) but not explainability. See
docs/known_issues.md, item 7.
"""

from typing import Dict

import numpy as np
import pandas as pd
import shap


def compute_shap_importance(model, X: pd.DataFrame, sample_size: int = 500, random_state: int = 42) -> pd.DataFrame:
    """Mean absolute SHAP value per feature, for a fitted tree-based model.

    Uses a random subsample for speed on large datasets (e.g. the 230K-row
    diabetes dataset) — adjust sample_size down further if this is still
    too slow locally.
    """
    X_sample = X.sample(n=min(sample_size, len(X)), random_state=random_state)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)

    # shap_values may be a list (per-class) for some classifiers; take the
    # positive-class values if so.
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    return pd.DataFrame({"Feature": X.columns, "Mean_Abs_SHAP": mean_abs_shap}).sort_values(
        "Mean_Abs_SHAP", ascending=False
    )


def compare_shap_rankings(baseline_shap: pd.DataFrame, doda_shap: pd.DataFrame) -> pd.DataFrame:
    """Merge two SHAP importance tables and report rank changes, mirroring
    the statistical-vs-clinical rank comparison already used in Phase 3.
    """
    b = baseline_shap.copy()
    d = doda_shap.copy()
    b["Baseline_SHAP_Rank"] = b["Mean_Abs_SHAP"].rank(ascending=False)
    d["DODA_SHAP_Rank"] = d["Mean_Abs_SHAP"].rank(ascending=False)

    merged = b[["Feature", "Baseline_SHAP_Rank"]].merge(
        d[["Feature", "DODA_SHAP_Rank"]], on="Feature", how="outer"
    )
    merged["Rank_Change"] = merged["Baseline_SHAP_Rank"] - merged["DODA_SHAP_Rank"]
    return merged.sort_values("Rank_Change", ascending=False)
