# Data Sources

`data/raw/` and `data/processed/` are gitignored — nothing in them is ever committed. This file is how anyone (including future-you) regenerates the data locally.

## Breast Cancer

- **Source:** scikit-learn built-in (`sklearn.datasets.load_breast_cancer`) — identical to the UCI Breast Cancer Wisconsin (Diagnostic) dataset.
- **How to get it:** no download needed; loaded directly via `sklearn.datasets.load_breast_cancer(as_frame=True)`.
- **License:** UCI ML Repository, freely redistributable for research use.

## Diabetes

- **Source:** Kaggle — "Diabetes Health Indicators Dataset" (Teboul, 2021), derived from the CDC's 2015 Behavioral Risk Factor Surveillance System (BRFSS).
- **URL:** https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset
- **How to get it:** download `diabetes_binary_health_indicators_BRFSS2015.csv` via Kaggle (requires free Kaggle account), place in `data/raw/`.
- **License:** CC0 (public domain) per Kaggle listing — verify before citing in the dissertation.
- **Rows / features:** 253,680 rows (pre-deduplication), 21 candidate features, binary target.

## Heart Disease

- **Source:** UCI Machine Learning Repository — Heart Disease dataset (Cleveland, or the combined 4-site version).
- **URL:** https://archive.ics.uci.edu/dataset/45/heart+disease
- **How to get it:** direct download from UCI, place in `data/raw/`.
- **License:** UCI ML Repository, freely redistributable for research use.
- **Note:** decide early whether to use the Cleveland-only subset (most commonly used, ~303 rows, cleanest) or the combined 4-site version (larger, more missing data) — document the choice in `docs/methodology.md`.

## CKD (Chronic Kidney Disease)

- **Source:** UCI Machine Learning Repository — Chronic Kidney Disease dataset.
- **URL:** https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease
- **How to get it:** direct download from UCI, place in `data/raw/`.
- **License:** UCI ML Repository, freely redistributable for research use.
- **Note:** ~400 rows, substantial missingness in several lab-value columns — plan an explicit imputation strategy before feature selection (see `docs/methodology.md`).

## Stroke (if used instead of / alongside CKD)

- **Source:** Kaggle — "Stroke Prediction Dataset".
- **URL:** https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset
- **License:** verify on Kaggle listing before citing.

## If a MIMIC-derived dataset is added later

MIMIC access is **credentialed and per-individual** — each team member needs their own CITI "Data or Specimens Only Research" course completion and a signed Data Use Agreement for the specific MIMIC version/derivative used. Access cannot be shared between team members, and raw or row-level MIMIC data can **never** be committed to this repo, public or private. Document the access process and any derived/aggregate summary files here, but never the underlying data.

---

### Checksums

Once real files are downloaded, add their SHA-256 checksums here so we can confirm we're both working from an identical file:

```
# example format:
# diabetes_binary_health_indicators_BRFSS2015.csv   sha256: <hash>
```
