# DODA: Decoupled Operator-Driven Architecture for Clinically Guided Feature Selection

Research repository for our MSc project evaluating whether a post-hoc, selector-independent clinical knowledge layer can recover clinically important features that conventional statistical feature selection misses — without sacrificing predictive performance — across multiple diseases and multiple base feature-selection algorithms.

Full research proposal: `docs/proposal.pdf`

---

## 1. Research Summary

Standard feature selection (ANOVA, LASSO, Mutual Information, mRMR, Random Forest Importance, Boruta) ranks variables by statistical association with the outcome only. This project tests whether adding a **decoupled, post-selection clinical re-weighting layer (DODA)** — applied _after_ statistical selection rather than baked into it — produces feature subsets that are simultaneously:

- more clinically meaningful (**clinical relevance**),
- comparably predictive (**Accuracy, Precision, Recall, F1, ROC-AUC**),
- more stable across resamples (**Jaccard similarity, rank correlation**), and
- more interpretable (**SHAP comparison**),

than the statistical baseline alone.

|     | RQ                                                                          | One-line version         |
| --- | --------------------------------------------------------------------------- | ------------------------ |
| RQ1 | Do conventional selectors consistently find clinically important variables? | Baseline check           |
| RQ2 | Can domain knowledge recover what statistical selection misses?             | The core claim           |
| RQ3 | Does that cost predictive performance?                                      | The trade-off check      |
| RQ4 | Does it generalize across datasets and selectors?                           | The generalization check |

**H₀:** No meaningful difference between statistical and clinically-guided feature selection.
**H₁:** Clinically-guided refinement is more clinically meaningful while maintaining comparable predictive performance.

---

## 2. Team & Dataset Ownership

| Person   | Datasets                | Diseases                              | Source                       |
| -------- | ----------------------- | ------------------------------------- | ---------------------------- |
| Angelina | Breast Cancer, CKD      | Breast cancer, Chronic kidney disease | sklearn/UCI, UCI             |
| Anandha  | Diabetes, Heart Disease | Type 2 diabetes, Cardiovascular       | Kaggle (CDC BRFSS 2015), UCI |

This repository is maintained by two collaborators conducting a joint MSc research project. — no formal ownership enforcement needed: if you're editing something in the other person's `notebooks/` folder, just mention it so nothing gets overwritten by accident.

---

## 3. Repository Structure

```
msc_doda_research/
│
├── README.md                     # you are here
├── CHANGELOG.md                  # hand-maintained log of meaningful changes (not automated)
├── CONTRIBUTING.md               # git workflow, branch/commit conventions
├── requirements.txt              # pinned pip dependencies — the single source of truth for the venv
├── .gitignore                    # excludes data/, checkpoints, notebook checkpoints, __pycache__
│
├── config/
│   └── clinical_weights/
│       ├── breast_cancer.yaml
│       ├── diabetes.yaml
│       ├── heart_disease.yaml
│       └── ckd.yaml              # one clinical weight dictionary per disease — cited, version-controlled
│
├── data/
│   ├── raw/                      # gitignored — never committed
│   ├── processed/                # gitignored — never committed
│   └── DATA_SOURCES.md           # download links, checksums, access notes
│
├── src/
│   └── doda/                     # shared, importable package — the ONE canonical implementation
│       ├── __init__.py
│       ├── selectors/            # lasso.py, mrmr.py, anova.py, mutual_info.py, rf_importance.py, boruta.py
│       ├── clinical_broker.py    # the DODA re-weighting layer
│       ├── evaluation.py         # metrics, CV loop, stability (Jaccard / rank correlation)
│       ├── explainability.py     # SHAP comparison utilities
│       └── utils.py
│
├── notebooks/
│   ├── angel/
│   │   ├── 01_breast_cancer_eda.ipynb
│   │   ├── 02_breast_cancer_doda.ipynb
│   │   ├── 03_ckd_eda.ipynb
│   │   └── 04_ckd_doda.ipynb
│   └── anandha/
│       ├── 01_diabetes_eda.ipynb
│       ├── 02_diabetes_doda.ipynb
│       ├── 03_heart_disease_eda.ipynb
│       └── 04_heart_disease_doda.ipynb
│
├── results/
│   ├── breast_cancer/
│   ├── diabetes/
│   ├── heart_disease/
│   └── ckd/                      # each disease owns its subfolder — no shared file two people write to
│
├── figures/
│   ├── breast_cancer/
│   ├── diabetes/
│   ├── heart_disease/
│   └── ckd/
│
├── tests/
│   └── test_clinical_broker.py   # e.g. "every feature has a weight; no silent default=1.0 fillna"
│
└── docs/
    ├── proposal.pdf
    ├── methodology.md            # shared write-up of the 6 pipeline phases, kept in sync with src/
    └── known_issues.md           # running list of methodological caveats to resolve before write-up
```

---

## 4. Setup

```bash
git clone <repo-url>
cd msc_doda_research

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

If you add a new package, add it to `requirements.txt` (with a pinned version) in the same commit that introduces the dependency, so the file always reflects what's actually needed to run the repo.

---

## 5. Pipeline (per dataset)

Every dataset follows the same six phases — this is what makes the "selector-independent" claim testable. Don't improvise a different structure per disease; if a phase genuinely needs to differ, document why in `docs/methodology.md`.

1. **Data ingestion & audit** — load, check missingness/duplicates/class balance, scale.
2. **Statistical feature selection** — run all selectors in `src/doda/selectors/`, per fold, under repeated stratified CV. Produces a consensus statistical ranking.
3. **Clinical Knowledge Layer (DODA)** — apply `src/doda/clinical_broker.py` using the disease's `config/clinical_weights/*.yaml` file. Produces the adjusted ranking.
4. **Top-K feature space construction** — slice both the baseline and DODA-adjusted rankings into Top-5/10/15/20.
5. **Model evaluation** — train Logistic Regression, Random Forest, XGBoost on both baseline and DODA feature spaces, under the same CV scheme.
6. **Multi-axis comparison** — predictive performance (both), clinical relevance / stability / explainability (DODA vs. baseline).

Each notebook should be numbered in the order it's meant to run (`01_`, `02_`, ...) and should import shared logic from `src/doda/` rather than redefining it locally — that's what keeps the four datasets comparable and keeps a bug fix in one place instead of four.

---

## 6. Git Workflow (see `CONTRIBUTING.md` for full detail)

- - Branches are optional for this project. Shared work may be committed directly to `main` as long as collaborators coordinate changes.
- **Strip notebook outputs before committing.** Set up `nbstripout` once (`nbstripout --install`) and this happens automatically — this alone prevents most notebook merge conflicts.
- Since it's just the two of you, informal is fine — but if you touch `src/doda/` (shared code) or the other person's `notebooks/` folder, mention it so nothing gets silently overwritten.
- One meaningful change per commit; commit message states _what_ and _why_ in one line.
- Update `CHANGELOG.md` for anything that would change a result (bug fix, weight change, new dataset, new selector) — not for typo fixes.

---

## 7. Data Access Notes

- Breast Cancer, Diabetes, Heart Disease, CKD: publicly downloadable, no credentialing required. Links and checksums in `data/DATA_SOURCES.md`.
- If a MIMIC-derived dataset is added later: **credentialed access is per-individual and non-transferable** — each of us would need our own CITI training and Data Use Agreement, and raw MIMIC data can never be committed to this repo (private or public). Document any such access step in `data/DATA_SOURCES.md` without including any data itself.

---

## 8. Known Methodological Caveats to Resolve Before Write-Up

Tracked in full in `docs/known_issues.md`. Carried over from the diabetes prototype review — check these are resolved for _every_ dataset, not just diabetes, before treating results as final:

- [ ] Single, source-cited clinical weight dictionary per disease (no undocumented post hoc overrides).
- [ ] Random Forest class-imbalance handling validated on recall, not just accuracy/ROC-AUC.
- [ ] Feature-selection stability metric corrected for chance agreement (or justified at the given sample size).
- [ ] Feature selection re-run inside each evaluation fold (or an explicit justification for a fixed feature space).

---

## 9. Citation & Attribution

If this repository contributes to academic work, please cite both the research proposal (`docs/proposal.pdf`) and the associated dissertation or publication once available. This repository documents the implementation, experimental pipeline, and reproducible evaluation framework for the DODA methodology.
