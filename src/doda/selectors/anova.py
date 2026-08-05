import pandas as pd
from sklearn.feature_selection import f_classif


def anova_operator(X_train, y_train, feature_names) -> pd.DataFrame:
    """Univariate ANOVA F-statistic per feature vs. target."""
    f_scores, _ = f_classif(X_train, y_train)
    return pd.DataFrame({"Feature": feature_names, "ANOVA": f_scores})
