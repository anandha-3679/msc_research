# Methodology

Living document — keep this in sync with `src/doda/` whenever the actual pipeline logic changes. If a notebook does something this document doesn't describe, one of the two is wrong; fix whichever is out of date.

## The Six Phases (applied identically to every dataset)

### Phase 1 — Data Ingestion & Preprocessing
Load raw data, audit missingness/duplicates/class balance, scale features (`RobustScaler` — chosen over standard scaling because most of our clinical features are skewed and/or contain outliers). Document dataset-specific decisions (e.g. CKD's missing-value imputation strategy) here as they're made.

### Phase 2 — Statistical Feature Selection
Run all selectors in `src/doda/selectors/` — LASSO, mRMR, ANOVA F-test, Mutual Information, Random Forest importance, Boruta — inside each fold of a repeated stratified cross-validation scheme (default: 5-fold, 5-repeat, 25 total iterations). Normalize each selector's scores to [0, 1] per fold, average into a `Final_Score`, and record both the per-fold Top-K selection (for Jaccard stability) and the full ranking (for rank stability).

> Doing selection *inside* each fold (not once on the full dataset) avoids the selection-bias problem described by Ambroise & McLachlan (2002) — keep this per-fold structure even as the pipeline is extended to new datasets.

### Phase 3 — Clinical Knowledge Layer (DODA)
Load the disease's `config/clinical_weights/<disease>.yaml` via `ClinicalKnowledgeBroker`, call `validate_against()` to confirm every dataset feature has a weight, then apply `apply_clinical_weights()` — an element-wise (Hadamard) product of the statistical `Final_Score` and the clinical weight.

**Rule:** exactly one weights file per disease, no in-notebook weight dictionaries, no undocumented overrides. If a weight needs to change, edit the YAML file and log why in `CHANGELOG.md`.

### Phase 4 — Feature Space Construction
Slice both the baseline (statistical-only) ranking and the DODA-adjusted ranking into Top-5/10/15/20 feature sets, for a total of 8 feature spaces per dataset (4 K-values × {baseline, DODA}).

### Phase 5 — Model Evaluation
Train Logistic Regression, Random Forest, and XGBoost on every feature space, under the same CV scheme as Phase 2. Report Accuracy, Precision, Recall, F1, ROC-AUC, PR-AUC, Balanced Accuracy, and MCC — not just accuracy/ROC-AUC, since accuracy alone can mask a recall collapse on imbalanced clinical targets (this happened with Random Forest in the diabetes prototype — watch for it on every dataset, not just diabetes).

### Phase 6 — Multi-Axis Comparison
- **Predictive performance**: baseline vs. DODA, all metrics from Phase 5.
- **Clinical relevance**: overlap between selected features and the disease's clinically-established feature list (define this list explicitly per disease, sourced — not ad hoc).
- **Feature stability**: mean pairwise Jaccard similarity (`evaluation.jaccard_stability`) AND mean-rank/rank-std (`evaluation.rank_stability`) — report both, since Jaccard alone can look artificially perfect (see `docs/known_issues.md`, item 4).
- **Explainability**: SHAP comparison (`explainability.py`) between baseline and DODA feature spaces.

## Open Design Decisions (fill in as agreed)

- [ ] Fixed cardinality (Top-K) for every selector, including Boruta, vs. letting Boruta use its natural "all-relevant" set — decide and document the rationale.
- [ ] Whether feature selection is re-run inside each Phase 5 fold (fully nested) or fixed once from the Phase 2 consensus ranking (current prototype approach) — see `docs/known_issues.md`, item 3.
- [ ] Per-disease clinically-established feature list — who sources it, and from where (guideline, expert consultation, prior published model).
