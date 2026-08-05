import pandas as pd
from sklearn.feature_selection import mutual_info_classif


def mutual_info_operator(X_train, y_train, feature_names, random_state: int = 42) -> pd.DataFrame:
    """Mutual information between each feature and the target.

    This selector is listed in the research proposal's Step 2 but was not
    present in the diabetes prototype notebook (which used LASSO, mRMR,
    ANOVA, and RF only). Added here so the full six-selector set from the
    proposal is actually implemented — see docs/known_issues.md, item 5.
    """
    mi_scores = mutual_info_classif(X_train, y_train, random_state=random_state)
    return pd.DataFrame({"Feature": feature_names, "MutualInfo": mi_scores})
