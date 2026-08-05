import pandas as pd
from mrmr import mrmr_classif


def mrmr_operator(X_train, y_train, feature_names, K: int = 10) -> pd.DataFrame:
    """Minimum-Redundancy-Maximum-Relevance selection (Peng, Long & Ding, 2005).

    mrmr_classif returns only a ranked list of the top K features (not a score
    for every feature), so non-selected features are scored 0 here. Note this
    means MRMR scores are not directly comparable in magnitude to the other
    three operators' scores before min-max normalization — see the ensembling
    caveat in docs/methodology.md.
    """
    selected = mrmr_classif(X=X_train, y=y_train, K=K)
    scores = [1.0 if f in selected else 0.0 for f in feature_names]
    # Preserve rank information rather than a flat 1/0 where possible:
    rank_map = {f: (K - i) for i, f in enumerate(selected)}
    scores = [rank_map.get(f, 0) for f in feature_names]
    return pd.DataFrame({"Feature": feature_names, "MRMR": scores})
