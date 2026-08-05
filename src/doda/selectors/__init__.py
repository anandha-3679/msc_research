"""
Statistical feature selection operators used in Phase 2 of the DODA pipeline.

Each operator takes (X_train, y_train, feature_names) and returns a DataFrame
with columns ["Feature", "<OPERATOR_NAME>"] so they can be merged together and
min-max normalized into a consensus score, exactly as in Phase 2 of the
prototype notebook.

Fill in each file's TODO with the corresponding logic from the diabetes
prototype (or write fresh — the interface is what matters for compatibility
across datasets, not the internal implementation).
"""
