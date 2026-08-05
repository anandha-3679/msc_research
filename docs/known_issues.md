# Known Methodological Issues

Running list of caveats identified from the diabetes prototype review. Check each one against **every** dataset (not just diabetes) before treating results as final for the dissertation. Move an item to "Resolved" with a date and short note once it's actually fixed in code — not just discussed.

## Open

1. **Clinical weight dictionaries need a real cited source.** The prototype had two inconsistent in-code dictionaries for diabetes (Stroke weight 1.0 vs. an undocumented override to 2.5), and the override's incompleteness silently inflated an unrelated feature (HvyAlcoholConsump) to a neutral default. Structural fix is in place (`src/doda/clinical_broker.py` raises instead of defaulting; one YAML file per disease). Still needed: an actual clinical source for every weight in every `config/clinical_weights/*.yaml` file — currently all marked `STATUS: DRAFT`.

2. **Random Forest + `class_weight="balanced"` can produce an accuracy/recall paradox.** In the diabetes prototype, RF recall collapsed from 0.71 to 0.15 as K increased from 5 to 20, while accuracy rose — because RF was increasingly predicting the majority class. Logistic Regression and XGBoost, on identical feature spaces, did not show this. Check for the same pattern on every dataset; consider a dedicated balanced-forest approach (undersampled bootstraps, or threshold-moving) rather than relying on `class_weight` alone if it recurs.

3. **Feature selection (Phase 2–4) and evaluation (Phase 5) are not fully independent.** The Top-K feature space is built from a ranking that aggregates across all 25 Phase-2 folds, then evaluated using a fresh 25-fold CV — so the feature set has effectively "seen" close to the whole dataset before evaluation starts. At n≈230K (diabetes) the resulting optimism is likely small; at smaller datasets (CKD, ~400 rows) it could matter more. Decide per-dataset whether to fully nest feature selection inside Phase 5's folds.

4. **A Jaccard stability score of exactly 1.000 needs scrutiny, not celebration.** This happened in the diabetes prototype and is plausible at n≈230K, but should be paired with a chance-corrected stability index (e.g. Kuncheva's index) or a bootstrap-subsample sensitivity check, especially for smaller datasets like CKD where perfect stability would be more surprising.

5. **The proposal specifies six selectors; the prototype only implemented four.** LASSO, mRMR, ANOVA, and RF were in the diabetes prototype; Mutual Information and Boruta were missing. Both are now stubbed in `src/doda/selectors/` — need testing against real data and a decision on how they're weighted into the Phase 2 consensus score (currently: simple average of whichever selectors are included — revisit if 6 selectors changes the balance described in `docs/methodology.md`).

6. **Boruta's natural output (all-relevant, variable-length) doesn't fit neatly into a fixed Top-K comparison.** The prototype truncated Boruta's confirmed set to a fixed 10, which likely explains its weaker relative performance — this may not be a fair comparison. Decide and document the approach in `docs/methodology.md`.

7. **Explainability axis (SHAP) wasn't implemented in the prototype at all.** Now stubbed in `src/doda/explainability.py` — needs testing and integration into the Phase 6 comparison for at least one dataset before assuming it works across all four.

8. **ROC/PR curves in the prototype were single-fold artifacts, not cross-validated averages** (a variable was overwritten every CV iteration, keeping only the last fold's curve). `evaluation.evaluate_feature_space()` now returns every fold's raw curve data (`_fold_curves`) — still needs a mean-curve-with-confidence-band plotting function added before this is fully resolved.

## Resolved

*(move items here as they're fixed — include date and one line on what changed)*
