"""
Phase 5 (model evaluation) and Phase 6 (stability analysis) shared logic.

Centralizing this — rather than each notebook writing its own copy of the
cross-validation loop — is what makes "baseline vs. DODA" comparisons across
four different diseases actually comparable. If you need dataset-specific
behavior, add a parameter here rather than forking the function in a notebook.
"""

from itertools import combinations
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)


METRIC_FUNCS = {
    "Accuracy": accuracy_score,
    "Precision": precision_score,
    "Recall": recall_score,
    "F1": f1_score,
    "Balanced_Accuracy": balanced_accuracy_score,
    "MCC": matthews_corrcoef,
}


def evaluate_feature_space(X_subset, y, model, cv) -> Dict[str, float]:
    """Run one (feature space, model) pair through the full CV scheme.

    Returns the mean of each metric across all folds. Unlike the prototype
    notebook's Phase 5 loop, this does NOT silently keep only the last fold's
    ROC/PR curve — see plot_mean_roc_curve() below for the fix to that
    specific limitation (see docs/known_issues.md, item 3).
    """
    metrics: Dict[str, List[float]] = {name: [] for name in METRIC_FUNCS}
    metrics["ROC_AUC"] = []
    metrics["PR_AUC"] = []
    fold_curves = []  # collect EVERY fold's curve, not just the last

    for train_idx, test_idx in cv.split(X_subset, y):
        X_train, X_test = X_subset.iloc[train_idx], X_subset.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        clf = clone(model)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]

        for name, func in METRIC_FUNCS.items():
            metrics[name].append(func(y_test, y_pred))
        metrics["ROC_AUC"].append(roc_auc_score(y_test, y_prob))
        metrics["PR_AUC"].append(average_precision_score(y_test, y_prob))

        fold_curves.append((y_test.values, y_prob))

    result = {name: float(np.mean(v)) for name, v in metrics.items()}
    result["_fold_curves"] = fold_curves  # keep raw data for mean-curve plotting
    return result


def jaccard_stability(selection_history: Iterable[List[str]]) -> float:
    """Mean pairwise Jaccard similarity across all fold selections.

    NOTE: a value at or very near 1.000 should be treated with suspicion,
    not celebration — see docs/known_issues.md, item 4, on why perfect
    stability can indicate the comparison isn't set up independently
    (e.g. Top-K built from a ranking that mixes information across the very
    folds being compared) rather than genuine robustness.
    """
    selection_history = list(selection_history)
    scores = []
    for set1, set2 in combinations(selection_history, 2):
        s1, s2 = set(set1), set(set2)
        scores.append(len(s1 & s2) / len(s1 | s2))
    return float(np.mean(scores))


def rank_stability(ranking_history: List[pd.DataFrame]) -> pd.DataFrame:
    """Mean rank and rank standard deviation per feature across folds.

    More information-rich than jaccard_stability() alone — a feature can have
    low Rank_STD (very stable position) even if it sits just outside a fixed
    Top-K cutoff, which Jaccard cannot show.
    """
    tables = []
    for i, df in enumerate(ranking_history):
        temp = df[["Feature", "Final_Score"]].copy()
        temp["Fold"] = i + 1
        temp["Rank"] = temp["Final_Score"].rank(ascending=False, method="average")
        tables.append(temp)

    rank_df = pd.concat(tables)
    return (
        rank_df.groupby("Feature")["Rank"]
        .agg(Mean_Rank="mean", Rank_STD="std")
        .reset_index()
        .sort_values("Rank_STD")
    )
