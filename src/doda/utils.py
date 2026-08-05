"""
Small shared helpers used across multiple pipeline phases / notebooks.
"""

from pathlib import Path

import pandas as pd


def load_clinical_weights_path(disease: str, config_dir: str = "config/clinical_weights") -> Path:
    """Resolve the path to a disease's clinical weight YAML file.

    Centralizing this means if the config folder ever moves, only one
    function needs to change, not every notebook.
    """
    path = Path(config_dir) / f"{disease}.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"No clinical weights file found at {path}. "
            f"Expected one YAML file per disease in {config_dir}/."
        )
    return path


def merge_operator_scores(*score_dfs: pd.DataFrame, on: str = "Feature") -> pd.DataFrame:
    """Outer-merge any number of selector score DataFrames on the Feature
    column, filling missing values with 0 (a feature not returned by a given
    selector is treated as having zero importance under that selector).
    """
    merged = score_dfs[0]
    for df in score_dfs[1:]:
        merged = merged.merge(df, on=on, how="outer")
    return merged.fillna(0)


def min_max_normalize(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """In-place-style min-max normalization of the given columns to [0, 1]."""
    df = df.copy()
    for col in columns:
        col_min, col_max = df[col].min(), df[col].max()
        span = col_max - col_min
        df[col] = 0.0 if span == 0 else (df[col] - col_min) / span
    return df
