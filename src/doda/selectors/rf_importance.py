import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def rf_operator(X_train, y_train, feature_names, n_estimators: int = 300) -> pd.DataFrame:
    """Random Forest mean-decrease-in-impurity importance.

    Note (see docs/known_issues.md, item 2): impurity-based RF importance is
    known to be biased toward high-cardinality / continuous features
    (Strobl et al., 2007). Consider adding permutation importance as a
    cross-check before finalizing results.
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators, class_weight="balanced", random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)
    return pd.DataFrame({"Feature": feature_names, "RF": model.feature_importances_})
