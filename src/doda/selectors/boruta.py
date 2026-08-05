import numpy as np
import pandas as pd
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier


def boruta_operator(X_train, y_train, feature_names, random_state: int = 42) -> pd.DataFrame:
    """Boruta all-relevant feature selection (Kursa & Rudnicki, 2010).

    This selector is listed in the research proposal's Step 2 but was only
    partially explored in the diabetes prototype (used, but truncated to a
    fixed Top-10 by internal ranking, which the earlier pipeline review
    flagged as unfair to Boruta's design intent — see docs/known_issues.md,
    item 6). This implementation returns Boruta's raw ranking; deciding
    whether/how to truncate to a fixed K is left to the evaluation phase,
    not baked into the selector itself.
    """
    rf = RandomForestClassifier(n_jobs=-1, class_weight="balanced", random_state=random_state)
    boruta_selector = BorutaPy(rf, n_estimators="auto", random_state=random_state, verbose=0)
    boruta_selector.fit(np.asarray(X_train), np.asarray(y_train))

    # ranking_: 1 = confirmed relevant, higher = eliminated earlier
    return pd.DataFrame({
        "Feature": feature_names,
        "Boruta": boruta_selector.ranking_.max() - boruta_selector.ranking_ + 1,
        "Boruta_Confirmed": boruta_selector.support_,
    })
