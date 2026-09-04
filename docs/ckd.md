# Clinical Weight Sourcing — Chronic Kidney Disease (UCI)

## What these weights are actually based on:

Same honesty flag as the breast cancer weight file: no guideline publishes a numeric importance weight for "blood urea" or "packed cell volume" directly. What exists, and what this mapping is built from, is the internationally-adopted clinical framework for how CKD is actually diagnosed and staged.

**KDIGO (Kidney Disease: Improving Global Outcomes) 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease** (_Kidney International_, 2024;105(4S):S117–S314) is the authoritative international guideline — the CKD equivalent of what the Nottingham/WHO grading system is for breast cancer. Its central diagnostic and staging framework is the **"CGA" classification**: (cite index="5-1">CKD is classified based on Cause, Glomerular filtration rate (GFR) category (G1–G5), and Albuminuria category (A1–A3)</cite>. The guideline's diagnostic criteria table is explicit about what counts as evidence of kidney damage: (cite index="11-1">albuminuria (ACR ≥30 mg/g), urine sediment abnormalities, persistent hematuria, electrolyte and other abnormalities due to tubular disorders, and decreased GFR (<60 mL/min per 1.73 m², present for at least 3 months)</cite>. GFR itself is estimated primarily from serum creatinine: (cite index="11-1">creatinine-based eGFR is still the first recommended method to estimate GFR</cite>.

That gives a direct, defensible correspondence for most of this dataset's 24 features — they map either onto the two CGA pillars themselves (creatinine → GFR; urine albumin → albuminuria), onto the guideline's explicit "markers of kidney damage" list (hematuria, electrolyte abnormalities), onto KDIGO's discussion of major causes/risk factors (diabetes, hypertension), or onto well-established CKD complications the guideline also covers (anemia, cardiovascular disease). A minority of features (urine sediment findings like pus cells and bacteria, white cell count) have a real but more indirect clinical rationale, noted below.

**As with the breast cancer file: this is a defensible, citable mapping from real guideline criteria, not a literal published weight table.** Treat it as "derived from the KDIGO CGA framework," and cite it that way.

---

## Weight logic by feature group

| Feature group                                                                                                                                               | What it measures                                                                                       | KDIGO correspondence                                                                                                                                                                                                                                         | Weight tier             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| `sc` (serum creatinine), `al` (albumin / albuminuria)                                                                                                       | The two pillars of CKD staging                                                                         | **Direct** — creatinine is the recommended first-line input to eGFR (the "G" in CGA); albuminuria is the "A" in CGA and one of the guideline's primary diagnostic criteria                                                                                   | **Highest** (1.0)       |
| `rbc` (red blood cells, urine)                                                                                                                              | Hematuria                                                                                              | Direct — "persistent hematuria" is explicitly listed as a marker of kidney damage in the diagnostic criteria table                                                                                                                                           | **High** (0.8)          |
| `htn` (hypertension), `dm` (diabetes mellitus)                                                                                                              | Major CKD causes/risk factors                                                                          | Direct — diabetes and hypertension are the two leading causes of CKD worldwide and are explicitly discussed in KDIGO's cause ("C") and risk-stratification framework                                                                                         | **High** (0.8)          |
| `bp` (blood pressure), `pot` (potassium), `bu` (blood urea)                                                                                                 | Continuous BP measurement; electrolyte status; traditional azotemia marker                             | Direct/near-direct — hypertension management is a core KDIGO treatment target; potassium abnormalities are explicitly named ("electrolyte...abnormalities due to tubular disorders"); BUN is a long-standing renal-function marker used alongside creatinine | **Moderate-high** (0.7) |
| `hemo` (hemoglobin), `bgr` (blood glucose), `sod` (sodium), `pcv` (packed cell volume), `cad` (coronary artery disease), `ane` (anemia), `pe` (pedal edema) | CKD-associated anemia; glycemic status; electrolyte status; cardiovascular comorbidity; fluid overload | Indirect but well-established — CKD-associated anemia and the CKD-cardiovascular link are both extensively covered in KDIGO's complications chapters, though these are downstream consequences rather than diagnostic/staging criteria themselves            | **Moderate** (0.6)      |
| `age`, `sg` (specific gravity), `rc` (red cell count)                                                                                                       | General risk stratification; urine concentrating ability; anemia proxy                                 | Indirect — age is a recognized risk-stratification factor in KDIGO's screening algorithm; specific gravity is part of routine urinalysis reflecting tubular function; red cell count correlates with the anemia signal `hemo`/`pcv` already carry            | **Moderate** (0.5–0.6)  |
| `su` (urine sugar), `pc` (pus cells), `pcc` (pus cell clumps), `appet` (appetite)                                                                           | Secondary diabetes marker; urinary tract infection/inflammation signs; nonspecific uremic symptom      | Weak/indirect — relevant to some CKD etiologies (e.g., pyelonephritis-related CKD) and to advanced-stage symptoms, but not part of the core CGA diagnostic framework                                                                                         | **Low-moderate** (0.4)  |
| `ba` (bacteria, urine), `wc` (white cell count, blood)                                                                                                      | Infection/inflammation markers                                                                         | Weakest correspondence — relevant to some secondary causes of kidney damage (e.g., infection-related) but general, non-CKD-specific markers                                                                                                                  | **Lowest** (0.3)        |

---

## Full weight table with per-feature notes

| Feature                       | Weight | Note                                                                                                        |
| ----------------------------- | ------ | ----------------------------------------------------------------------------------------------------------- |
| sc (serum creatinine)         | 1.0    | Primary input to eGFR — the "G" in KDIGO's CGA staging framework                                            |
| al (albumin)                  | 1.0    | Albuminuria — the "A" in CGA; one of two primary CKD diagnostic criteria                                    |
| rbc (red blood cells, urine)  | 0.8    | Hematuria — explicitly named marker of kidney damage                                                        |
| htn (hypertension)            | 0.8    | Leading CKD cause/accelerant; core KDIGO management target                                                  |
| dm (diabetes mellitus)        | 0.8    | Leading cause of CKD worldwide                                                                              |
| bp (blood pressure)           | 0.7    | Continuous form of the hypertension signal above                                                            |
| pot (potassium)               | 0.7    | Electrolyte abnormality explicitly named in diagnostic criteria; hyperkalemia is a recognized CKD emergency |
| bu (blood urea)               | 0.7    | Traditional renal-function marker, used alongside creatinine                                                |
| hemo (hemoglobin)             | 0.7    | Primary CKD-associated anemia marker                                                                        |
| bgr (blood glucose random)    | 0.6    | Glycemic control marker, tied to diabetes as leading CKD cause                                              |
| sod (sodium)                  | 0.6    | Electrolyte abnormality explicitly named in diagnostic criteria                                             |
| pcv (packed cell volume)      | 0.6    | Correlates with hemoglobin/anemia                                                                           |
| cad (coronary artery disease) | 0.6    | CKD-cardiovascular disease link is a major KDIGO complications theme                                        |
| ane (anemia flag)             | 0.6    | Same clinical concept as hemo/pcv, as a categorical label                                                   |
| pe (pedal edema)              | 0.6    | Recognized sign of fluid overload / reduced GFR                                                             |
| age                           | 0.6    | Recognized risk-stratification factor in KDIGO's screening algorithm                                        |
| sg (specific gravity)         | 0.5    | Urine concentrating ability — part of routine urinalysis, tubular function proxy                            |
| rc (red blood cell count)     | 0.5    | Correlates with the anemia signal already captured by hemo/pcv                                              |
| su (sugar, urine)             | 0.4    | Secondary/less direct diabetes marker than bgr                                                              |
| pc (pus cells, urine)         | 0.4    | Suggests infection/inflammation; relevant to some CKD etiologies                                            |
| pcc (pus cell clumps)         | 0.4    | Same rationale as pc, slightly more specific for infection                                                  |
| appet (appetite)              | 0.4    | Nonspecific uremic symptom, typically seen in advanced CKD                                                  |
| ba (bacteria, urine)          | 0.3    | Infection marker; weak, non-CKD-specific correspondence                                                     |
| wc (white cell count, blood)  | 0.3    | General inflammation/infection marker; least CKD-specific feature in the set                                |

---

## Sources

1. Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease. _Kidney International_, 2024;105(4S):S117–S314. https://www.kidney-international.org/article/S0085-2538(23)00766-4/fulltext
2. KDIGO 2024 Clinical Practice Guideline for CKD — full guideline PDF. https://kdigo.org/wp-content/uploads/2024/03/KDIGO-2024-CKD-Guideline.pdf
3. Levin, A., Ahmed, S., Carrero, J. J., et al. Executive summary of the KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease: known knowns and known unknowns. _Kidney International_ (ScienceDirect), March 2024.
4. Torres Rodriguez, S., & Gautam, M. (2024). "The KDIGO CKD 2024 Guidelines Part 1: Evaluation and Risk Stratification." NephJC — includes the Criteria for Chronic Kidney Disease Diagnosis table (albuminuria, urine sediment abnormalities, persistent hematuria, electrolyte abnormalities, decreased GFR) referenced throughout this document.
5. KDOQI US Commentary on the KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of CKD. _American Journal of Kidney Diseases_, November 2024.
6. Rubini, M., Soundarapandian, P., & Eswaran, P. (2015). Chronic Kidney Disease [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5G020 — the origin dataset; defines the exact 24 features weighted above.

## Status

**DRAFT — mapped from the KDIGO CGA framework by the analyst, not independently reviewed by a nephrologist.** As with the breast cancer file, the two highest-confidence entries are `sc` and `al` — they map directly onto KDIGO's own named staging pillars, with no interpretive judgment required. The weights carrying the most interpretive judgment, and therefore most in need of a domain-expert check before use in a reported result, are the mid-tier entries (`age`, `sg`, `cad`, `pe`, `appet`) — these have a real but qualitative connection to CKD risk/management rather than a table KDIGO publishes in numeric form.
