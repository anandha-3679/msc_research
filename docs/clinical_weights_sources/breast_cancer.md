# Clinical Weight Sourcing — Breast Cancer (Wisconsin Diagnostic)

## What these weights are actually based on (read this first)

No guideline — WHO or otherwise — publishes a numeric importance weight for a specific pixel-derived feature like "worst concave points." That doesn't exist and shouldn't be claimed. What _does_ exist, and what these weights are built from, is this:

**WHO's Classification of Tumours Editorial Board (Breast Tumours, 5th edition, 2019, IARC) mandates the Nottingham Histologic Grade** (the Elston–Ellis modification of the Scarff–Bloom–Richardson system) as the required grading method for invasive breast carcinoma — endorsed alongside the College of American Pathologists, the Commission on Cancer, and the National Accreditation Program for Breast Centres [1, 2].

Nottingham grading scores three components (1–3 each): **tubule/gland formation**, **nuclear pleomorphism**, and **mitotic count**. Of these three, only nuclear pleomorphism is something the Wisconsin dataset's 30 features can plausibly measure — tubule formation is a tissue-architecture judgment and mitotic count requires counting dividing cells, neither of which this dataset's single-nucleus measurements capture. So the mapping used here is specifically: **do these 30 features correspond to what pathologists are instructed to look at when scoring nuclear pleomorphism, and if so, how directly?**

The College of American Pathologists' reporting protocol operationalizes nuclear pleomorphism scoring explicitly in terms of nuclear **size**, **shape/outline regularity**, and **chromatin appearance** [3]:

- Score 1: "nuclei small with little increase in size... regular outlines, uniform nuclear chromatin, little variation in size"
- Score 3: "markedly enlarged... nucleoli often prominent... marked variation in size and shape"

That's the criteria table these weights are derived from. Separately, the dataset's own origin paper — Street, Wolberg & Mangasarian (1993), the paper that built this exact feature set from digitized FNA images — independently highlighted `worst perimeter`, `worst area`, and `worst concave points` as the strongest discriminators between benign and malignant samples in their own analysis [4, 5], which is used below as a second, independent check on the weighting, not the primary source.

**This is a defensible, citable mapping — not a literal published weight table.** Treat it as "derived from Nottingham/CAP nuclear pleomorphism criteria, cross-checked against the dataset's origin paper," and cite it that way rather than as "WHO weights."

---

## Weight logic by feature group

| Feature group                 | What it measures                                                  | Nottingham/CAP correspondence                                                                                                                                                                                         | Weight tier                              |
| ----------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `radius`, `perimeter`, `area` | Nuclear **size**                                                  | Direct — size increase is the first criterion listed for pleomorphism scoring (score 1 vs. 3 hinges on size increase)                                                                                                 | **Highest** (0.9 mean / 1.0 worst)       |
| `concavity`, `concave points` | Nuclear **outline irregularity** (indentations in the boundary)   | Direct — "regular outlines" (score 1) vs. irregular is the second explicit criterion                                                                                                                                  | **Highest** (0.9 mean / 1.0 worst)       |
| `compactness`                 | Combined perimeter²/area — a derived size+shape distortion metric | Indirect but closely related — mathematically increases with both enlargement and irregularity, both explicit criteria, but is a composite/engineered statistic rather than something a pathologist directly assesses | **High-moderate** (0.7 mean / 0.8 worst) |
| `symmetry`                    | Bilateral shape symmetry of the nucleus                           | Indirect — shape-related, part of the general "variation in size and shape" language, but not named as its own criterion the way outline regularity is                                                                | **Moderate** (0.5 mean / 0.6 worst)      |
| `texture`                     | Gray-level (chromatin pattern) variance within the nucleus        | Indirect proxy — chromatin appearance ("uniform" vs. not) is part of the CAP criteria narrative, but gray-scale standard deviation is a rough computational proxy for what a pathologist reads qualitatively          | **Moderate** (0.5 mean / 0.6 worst)      |
| `smoothness`                  | Local variation in radial distance (membrane contour smoothness)  | Weak/secondary — related to outline regularity but not the primary irregularity signal (that's concavity); more a supporting descriptor                                                                               | **Moderate-low** (0.4 mean / 0.5 worst)  |
| `fractal dimension`           | Boundary contour complexity ("coastline" measure)                 | No correspondence in Nottingham/CAP criteria at all — this is a purely mathematical texture-complexity feature from the original engineering paper [4], with no established grading-guideline counterpart found       | **Lowest** (0.3 mean / 0.3 worst)        |

## Why `worst` outranks `mean`, and both outrank `error` (standard error)

This isn't an arbitrary convention — it follows directly from how pathologists are instructed to score pleomorphism. The CAP protocol scores nuclear pleomorphism based on the **most atypical cells observed**, not the average appearance across the sample [3] — which is exactly what the `worst` (largest/most extreme) feature values represent in this dataset, versus `mean` (average across all measured nuclei). `error` (standard error across nuclei) captures cell-to-cell _variability_, which the CAP criteria do mention ("variation in size and shape") but only as a secondary descriptor layered on top of the primary size/shape assessment — hence the lowest weight tier of the three.

---

## Full weight table with per-feature notes

| Feature                 | Weight | Note                                                                                         |
| ----------------------- | ------ | -------------------------------------------------------------------------------------------- |
| worst radius            | 1.0    | Size, worst-nucleus form — primary pleomorphism criterion                                    |
| worst perimeter         | 1.0    | Size — primary criterion; also the feature Street et al. (1993) specifically highlighted [4] |
| worst area              | 1.0    | Size — primary criterion; also highlighted in the origin dataset paper [4, 5]                |
| worst concavity         | 1.0    | Outline irregularity, worst-nucleus form — primary pleomorphism criterion                    |
| worst concave points    | 1.0    | Outline irregularity — primary criterion; specifically flagged as a top discriminator in [5] |
| mean radius             | 0.9    | Size, average form                                                                           |
| mean perimeter          | 0.9    | Size, average form                                                                           |
| mean area               | 0.9    | Size, average form                                                                           |
| mean concavity          | 0.9    | Outline irregularity, average form                                                           |
| mean concave points     | 0.9    | Outline irregularity, average form                                                           |
| worst compactness       | 0.8    | Composite size+shape distortion metric, worst form                                           |
| mean compactness        | 0.7    | Composite size+shape distortion metric, average form                                         |
| worst texture           | 0.6    | Chromatin-pattern proxy, worst form                                                          |
| worst symmetry          | 0.6    | Shape symmetry, worst form                                                                   |
| mean texture            | 0.5    | Chromatin-pattern proxy, average form                                                        |
| mean symmetry           | 0.5    | Shape symmetry, average form                                                                 |
| radius error            | 0.5    | Size variability — "variation in size" is explicitly named in CAP criteria                   |
| perimeter error         | 0.5    | Size variability                                                                             |
| area error              | 0.5    | Size variability                                                                             |
| worst smoothness        | 0.5    | Membrane contour smoothness, secondary to concavity, worst form                              |
| mean smoothness         | 0.4    | Membrane contour smoothness, average form                                                    |
| concavity error         | 0.4    | Outline-irregularity variability                                                             |
| concave points error    | 0.4    | Outline-irregularity variability                                                             |
| texture error           | 0.3    | Chromatin-pattern variability                                                                |
| compactness error       | 0.3    | Composite-metric variability                                                                 |
| symmetry error          | 0.3    | Shape-symmetry variability                                                                   |
| mean fractal dimension  | 0.3    | No Nottingham/CAP correspondence identified — engineering feature only                       |
| worst fractal dimension | 0.3    | No Nottingham/CAP correspondence identified — engineering feature only                       |
| smoothness error        | 0.2    | Weakest criterion correspondence, plus variability discount                                  |
| fractal dimension error | 0.2    | No correspondence, plus variability discount                                                 |

---

## Sources

1. WHO Classification of Tumours Editorial Board. _Breast Tumours_, 5th Edition. Lyon: International Agency for Research on Cancer (IARC), 2019.
2. Mohd Zain, A. H., Mohd Isa, S. A., Che Jalil, N. A., Mohd Hairon, S., & Abrar, S. S. (2025). Modification of the nuclear pleomorphism score in the Modified Bloom-Richardson grading for invasive breast cancer. _PLOS ONE_. https://doi.org/10.1371/journal.pone.0327860 — confirms Nottingham grading's endorsement by WHO, CAP, CoC, and NAPBC.
3. College of American Pathologists. _Protocol for the Examination of Biopsy Specimens From Patients With Invasive Carcinoma of the Breast_ — Nottingham combined histologic grade criteria, nuclear pleomorphism scoring definitions (Score 1 vs. Score 3 descriptions).
4. Street, W. N., Wolberg, W. H., & Mangasarian, O. L. (1993). Nuclear feature extraction for breast tumor diagnosis. _Proceedings of IS&T/SPIE International Symposium on Electronic Imaging: Science and Technology_, 1905, 861–870. — origin paper for this exact dataset; defines all 10 base nuclear features (radius, texture, perimeter, area, smoothness, compactness, concavity, concave points, symmetry, fractal dimension) and their mean/worst/SE computation.
5. Wolberg, W. H., Street, W. N., Heisey, D. M., & Mangasarian, O. L. (1995). Computer-derived nuclear features distinguish malignant from benign breast cytology. _Human Pathology_, 26, 792–796. — follow-up validation study identifying which computed features carried the most diagnostic weight (worst area, worst perimeter, worst concave points among them).

## Status

**DRAFT — mapped from published grading criteria by the analyst, not independently reviewed by a pathologist or oncologist.** Before this is used in any reported result, it should ideally be checked by someone with clinical pathology background — particularly the `compactness`, `symmetry`, and `texture` tiers, which required the most interpretive judgment to map from qualitative criteria language to a 0–1 weight. The `fractal dimension` weight (lowest tier, no criteria correspondence found) is the most defensible entry in this table precisely because the absence of correspondence is easy to verify — the middle-tier entries are where a domain expert's judgment would add the most value.
