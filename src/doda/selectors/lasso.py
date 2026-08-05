import pandas as pd
from sklearn.linear_model import LogisticRegression


def lasso_operator(X_train, y_train, feature_names, C: float = 0.1) -> pd.DataFrame:
    """L1-penalized logistic regression; |coefficient| as importance score."""
    model = LogisticRegression(
        penalty="l1", C=C, solver="liblinear", max_iter=1000, random_state=42
    )
    model.fit(X_train, y_train)
    scores = abs(model.coef_[0])
    return pd.DataFrame({"Feature": feature_names, "LASSO": scores})
