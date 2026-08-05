# Changelog

All notable, result-affecting changes to this project are recorded here, in reverse chronological order. This is maintained by hand — add an entry whenever a bug fix, weight change, new dataset, or new selector could change a previously reported number.

Format per entry: `YYYY-MM-DD — who — what changed and why`.

## [Unreleased]

- 2026-08-02 — setup — Initial repo scaffold created (folder structure, requirements.txt, config templates, src/doda package skeleton, starter tests).
- 2026-08-02 — setup — Switched dependency management from conda (environment.yml) to venv + requirements.txt.
- 2026-08-02 — setup — Finalized dataset ownership: Angelina (Breast Cancer, CKD), Anandha (Diabetes, Heart Disease). Removed formal ownership-enforcement rule — two-person collaboration, informal coordination instead.

---

### Template for future entries

```
## [Unreleased]

- YYYY-MM-DD — <name> — <what changed>. <why it matters / what result it affects>.
```

### Example of the kind of entry this file is for

```
- 2026-08-15 — anandha — Fixed diabetes.yaml: HvyAlcoholConsump was missing from the
  clinical weight dictionary and silently defaulted to 1.0 instead of the intended 0.2.
  This changes the Top-10 diabetes feature set reported in results/diabetes/.
```
