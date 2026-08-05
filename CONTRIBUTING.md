# Contributing Guide (Angelina & Anandha)

This is a two-person research repo, not a public open-source project — this document is short on purpose. Its only job is to stop us from stepping on each other's files.

## 1. One-time setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
nbstripout --install            # run this ONCE per local clone — strips notebook outputs automatically on commit
```

`nbstripout --install` is the single most important line in this file. It configures git so that every time either of us commits a `.ipynb`, the *output cells* (plots, printed tables, execution counts) are stripped before the diff is generated. Code and markdown cells are untouched. This is what prevents 90% of notebook merge conflicts — without it, two people running the same notebook produce two different binary blobs even if the code is identical.

## 2. Branching

- Never commit directly to `main`.
- Branch name format: `feature/<dataset>-<short-description>`, e.g. `feature/diabetes-fix-clinical-weights`, `feature/heart-disease-eda`.
- If your change touches shared code (`src/doda/`), keep the branch small and focused — one logical change — so the other person can review it in a few minutes, not an hour.

## 3. Commit messages

One line, present tense, states what and why:

```
Fix HvyAlcoholConsump silently defaulting to weight=1.0 in diabetes.yaml

Missing key in the second clinical_weights dict caused fillna(1.0) to
override the intended 0.2 weight from the ClinicalKnowledgeBroker class.
```

## 4. Pull requests (even for a two-person team)

Still open a PR instead of merging directly, even for small changes — it gives the other person a chance to see what changed before it lands in `main`, and it gives *you* a paper trail for the dissertation's methodology section later. Self-merge is fine after a quick look; the point is visibility, not approval gatekeeping.

## 5. Working across the repo

This is just the two of you working on a shared research experiment, so there's no formal access-control rule — both of you can touch anything. The only practical guidance:

- If you're editing the other person's dataset files (`notebooks/anandha/` or `notebooks/angelina/`, their `results/`, `figures/`, or `config/clinical_weights/*.yaml`), just say so (commit message or a quick message to each other) so nothing gets overwritten by accident.
- Changes to `src/doda/` (shared code) affect both of you — a quick heads-up before or right after committing is enough, no formal review process needed.
- More tests in `tests/` are always welcome from either of you.
- Keep `docs/methodology.md` in sync if you change how a phase actually works in code.

## 6. Data

Never commit anything in `data/raw/` or `data/processed/` — they're gitignored for a reason (repo size, and for any credentialed-access dataset, licence compliance). Document how to *regenerate* the data locally in `data/DATA_SOURCES.md` instead.

## 7. Changelog

Add a line to `CHANGELOG.md` for anything that would change a reported result: a bug fix, a clinical weight change, a new dataset, a new selector added. Skip it for typo fixes, formatting, comments.
