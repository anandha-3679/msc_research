# Clinical Weight Sourcing — Diabetes (BRFSS)

## What these weights are actually based on

The clinical weights used in DODA are **not published numerical risk coefficients** from the American Diabetes Association (ADA), CDC, or another clinical guideline.

Clinical guidelines identify and discuss important risk factors for type 2 diabetes, but they do not provide a table such as:

> `BMI = 1.0`, `HighBP = 1.0`, `Sex = 0.2`

Therefore, the numerical values used in this study should **not** be described as "ADA weights" or as validated clinical effect sizes.

Instead, the weights are treated as **normalized prior-knowledge scores**. They encode the relative clinical relevance of the variables based on established diabetes risk-factor evidence and the clinical meaning of the variables available in the dataset.

The weighting process therefore follows:

**Clinical guidelines and literature → identify clinical relevance → assign qualitative relevance tiers → convert tiers to normalized 0–1 prior weights → DODA clinical operator**

The purpose of these weights is to provide DODA with **domain-informed prior knowledge**, rather than to claim that the weights represent causal effects or epidemiological coefficients.

---

## Evidence supporting the clinical relevance of the variables

The American Diabetes Association (ADA) Standards of Care 2026 identifies several factors relevant to screening for prediabetes and type 2 diabetes.

For adults with overweight or obesity, the ADA identifies **history of cardiovascular disease, hypertension, dyslipidemia, and physical inactivity** among the risk factors that should be considered when assessing diabetes risk. The ADA also recommends screening beginning at age 35 for other adults, explicitly identifying **age as a major risk factor for diabetes**.

The ADA further describes the relationship between prediabetes, obesity, dyslipidemia, hypertension, cardiovascular disease, and other cardiometabolic risk factors.

These recommendations provide the primary clinical basis for assigning higher prior-knowledge weights to variables such as:

- `BMI`
- `HighBP`
- `HighChol`
- `Age`
- `HeartDiseaseorAttack`
- `Stroke`
- `PhysActivity`

However, several variables in the BRFSS dataset are **proxies rather than direct clinical risk factors**. Examples include `GenHlth`, `DiffWalk`, `PhysHlth`, `Income`, `Education`, and healthcare-access variables.

These variables are therefore weighted according to their **indirect clinical or contextual relevance**, rather than being treated as equivalent to established diabetes risk factors.

---

## Weighting principle

The numerical weights are interpreted as **ordinal clinical relevance tiers**, not precise effect sizes.

| Weight range | Interpretation |
|---|---|
| **1.0** | Very high clinical relevance |
| **0.9** | High clinical relevance |
| **0.8** | Moderately high clinical relevance |
| **0.5–0.7** | Moderate clinical relevance |
| **0.3–0.4** | Low-to-moderate / indirect relevance |
| **0.2** | Low or weak direct clinical relevance |

Thus, a weight of `1.0` does **not** mean that the feature is exactly twice as clinically important as a feature with weight `0.5`.

Instead, the values represent predefined **relative prior-knowledge tiers** supplied to the DODA clinical operator.

---

# Current Clinical Weight Configuration

The following weights were used in the reported DODA experiments:

| Feature | Weight | Clinical interpretation |
|---|---:|---|
| `HighBP` | **1.0** | Major cardiometabolic risk factor and explicitly identified by ADA as a diabetes screening risk factor |
| `HighChol` | **0.9** | Dyslipidemia-related cardiometabolic risk |
| `BMI` | **1.0** | Overweight/obesity is a major established risk factor for type 2 diabetes |
| `GenHlth` | **1.0** | Overall health-status proxy representing accumulated disease burden |
| `PhysHlth` | **0.8** | Proxy for physical health burden and comorbidity |
| `MentHlth` | **0.5** | Indirect health-status/behavioral proxy |
| `Age` | **0.9** | Established diabetes risk factor; ADA identifies age as a major risk factor |
| `HeartDiseaseorAttack` | **1.0** | Indicator of established cardiovascular disease, which is an ADA-recognized diabetes screening risk factor |
| `Stroke` | **1.0** | Indicator of established vascular disease and cardiometabolic burden |
| `DiffWalk` | **0.9** | Functional-health proxy associated with physical limitation and overall disease burden |
| `Smoker` | **0.6** | Lifestyle and cardiometabolic risk factor |
| `Income` | **0.3** | Socioeconomic/contextual proxy rather than direct biological risk |
| `Education` | **0.3** | Socioeconomic/health-literacy proxy |
| `Sex` | **0.2** | Demographic variable with comparatively weaker direct relevance in this feature set |
| `Fruits` | **0.2** | Dietary/lifestyle proxy represented by a relatively coarse binary variable |
| `Veggies` | **0.2** | Dietary/lifestyle proxy represented by a relatively coarse binary variable |
| `HvyAlcoholConsump` | **0.2** | Lifestyle proxy with weaker direct representation in this dataset |
| `AnyHealthcare` | **0.2** | Healthcare-access/utilization proxy rather than biological risk |
| `NoDocbcCost` | **0.2** | Healthcare-access/socioeconomic proxy |
| `CholCheck` | **0.4** | Preventive healthcare-utilization indicator rather than direct biological risk |
| `PhysActivity` | **0.4** | Established diabetes-related lifestyle factor, but represented here using a simple binary BRFSS variable |

---

# Detailed Evidence-Based Rationale

## 1. BMI — Weight = 1.0

`BMI` receives the highest prior-knowledge tier because overweight and obesity are among the strongest and most consistently recognized risk factors for type 2 diabetes.

The ADA 2026 Standards of Care recommends considering diabetes testing in adults with overweight or obesity who have one or more additional diabetes risk factors. The guideline also identifies obesity and insulin resistance as important components of diabetes risk.

Therefore:

**Clinical evidence → strong**

**DODA prior weight → 1.0**

The value `1.0` should be interpreted as the highest prior-knowledge tier, not as an ADA numerical coefficient.

---

## 2. HighBP — Weight = 1.0

`HighBP` represents hypertension.

The ADA explicitly lists hypertension (≥130/80 mmHg or treatment for hypertension) among the risk factors that should be considered when screening adults for prediabetes and type 2 diabetes.

Hypertension is also closely associated with cardiometabolic risk and commonly coexists with obesity, insulin resistance, and dyslipidemia.

Therefore:

**Clinical evidence → strong**

**DODA prior weight → 1.0**

---

## 3. HighChol — Weight = 0.9

`HighChol` represents a history of high cholesterol and acts as a proxy for dyslipidemia.

The ADA identifies dyslipidemia, including abnormal HDL and triglyceride levels, among the risk factors considered in diabetes screening and emphasizes cardiovascular-risk management in people with diabetes and prediabetes.

Because the BRFSS variable is a coarse indicator of high cholesterol rather than a complete lipid profile, it is assigned a slightly lower prior tier than BMI and hypertension.

**Clinical evidence → strong/moderate**

**DODA prior weight → 0.9**

---

## 4. Age — Weight = 0.9

Age is a well-established diabetes risk factor.

The ADA 2026 Standards state that age is a major risk factor for diabetes and recommend screening for all other adults beginning at age 35.

Therefore `Age` receives a high prior-knowledge weight.

**Clinical evidence → strong**

**DODA prior weight → 0.9**

---

## 5. HeartDiseaseorAttack — Weight = 1.0

`HeartDiseaseorAttack` represents a history of cardiovascular disease.

The ADA explicitly includes a **history of cardiovascular disease** among the risk factors considered when screening adults for diabetes.

The variable is therefore treated as an important marker of cardiometabolic disease burden.

**Clinical evidence → strong**

**DODA prior weight → 1.0**

Importantly, this weight does **not** imply that cardiovascular disease directly causes diabetes. It represents the clinical relevance of an established cardiovascular-disease history as part of the patient's overall cardiometabolic risk profile.

---

## 6. Stroke — Weight = 1.0

`Stroke` represents a history of stroke.

Stroke is not treated here as a primary causal diabetes predictor. Instead, it is used as a marker of **established vascular disease and cardiometabolic burden**.

The ADA discusses stroke and other vascular events in the context of cardiovascular disease and cardiometabolic risk, including the relationship between insulin resistance, prediabetes, and vascular disease.

Therefore, `Stroke` is assigned a high clinical-prior weight.

**Clinical interpretation → vascular/comorbidity proxy**

**DODA prior weight → 1.0**

---

## 7. GenHlth — Weight = 1.0

`GenHlth` is a self-reported overall-health measure.

It is **not a canonical ADA diabetes risk factor**.

Its high weight therefore should not be described as a guideline-derived diabetes weight.

Instead, it represents a **dataset-level clinical proxy for overall disease burden**.

Because the variable summarizes an individual's perceived general health, it can provide contextual information about multiple underlying health conditions that may coexist with diabetes.

**Clinical evidence → indirect**

**DODA interpretation → overall health-burden proxy**

**DODA prior weight → 1.0**

This distinction is important when reporting the methodology.

---

## 8. PhysHlth — Weight = 0.8

`PhysHlth` captures the number of days in which physical health was reported as poor.

This is not a direct diagnostic or guideline-defined diabetes risk factor.

It is therefore treated as an **indirect health-burden proxy**.

Its weight is lower than the strongest established risk factors but remains relatively high because poor physical health can reflect multiple chronic conditions and functional limitations.

**Clinical evidence → indirect/moderate**

**DODA prior weight → 0.8**

---

## 9. DiffWalk — Weight = 0.9

`DiffWalk` represents difficulty walking or performing physical activities.

This variable is treated as a **functional-health proxy**, rather than a direct diabetes risk factor.

Its relevance is related to physical limitation, reduced mobility, overall disease burden, and potential interaction with physical inactivity.

Because the variable does not directly measure diabetes risk, its high weight represents prior clinical relevance of functional limitation rather than an established diabetes coefficient.

**Clinical evidence → indirect**

**DODA prior weight → 0.9**

---

## 10. PhysActivity — Weight = 0.4

`PhysActivity` indicates whether the individual reported physical activity.

Physical inactivity is explicitly identified by the ADA as a diabetes screening risk factor. The ADA also recommends evaluating physical activity and sedentary behavior among people with or at risk for diabetes.

Therefore, the variable has clear clinical relevance.

However, the BRFSS variable is a relatively coarse binary representation of activity and does not capture activity duration, intensity, frequency, or sedentary time.

Consequently, the current configuration uses a moderate/low prior weight:

**Clinical evidence → strong**

**Variable representation → coarse**

**DODA prior weight → 0.4**

This weight should therefore be interpreted as a **conservative encoding of clinical relevance**, not as an assertion that physical activity is clinically unimportant.

---

## 11. Smoker — Weight = 0.6

`Smoker` represents tobacco exposure.

Smoking is an important modifiable health behavior and is relevant to overall cardiometabolic risk.

However, compared with BMI, hypertension, age, and established cardiovascular disease, its role as a direct predictor in this particular feature set is less central.

Therefore:

**Clinical relevance → moderate**

**DODA prior weight → 0.6**

---

## 12. MentHlth — Weight = 0.5

`MentHlth` captures self-reported poor mental-health days.

Mental health is relevant to overall health and health behavior, but this variable is not a direct guideline-defined diabetes risk factor.

It is therefore assigned a moderate prior weight.

**Clinical evidence → indirect**

**DODA prior weight → 0.5**

---

## 13. CholCheck — Weight = 0.4

`CholCheck` indicates whether cholesterol was checked.

This variable reflects **healthcare utilization/preventive-care behavior**, rather than a biological characteristic that directly increases diabetes risk.

Therefore it receives a lower prior weight.

**Clinical evidence → contextual**

**DODA prior weight → 0.4**

---

## 14. Income and Education — Weight = 0.3

`Income` and `Education` are socioeconomic/contextual variables.

They can influence health behaviors, healthcare access, prevention, and disease management, but they are not direct biological measures of diabetes risk.

Consequently, they receive low-to-moderate prior weights.

**Clinical evidence → indirect/contextual**

**DODA prior weight → 0.3**

---

## 15. Fruits and Veggies — Weight = 0.2

`Fruits` and `Veggies` represent simplified dietary-behavior variables.

Dietary behavior is relevant to diabetes prevention and metabolic health. However, these BRFSS variables are binary and provide only a limited representation of dietary quality.

Therefore, they receive low prior weights.

**Clinical evidence → lifestyle-related**

**Variable representation → coarse**

**DODA prior weight → 0.2**

---

## 16. HvyAlcoholConsump — Weight = 0.2

`HvyAlcoholConsump` represents heavy alcohol consumption.

Alcohol consumption can influence metabolic and cardiovascular health, but the binary variable used here provides limited information about dose, duration, and drinking pattern.

Therefore, it receives a low prior weight.

**Clinical evidence → indirect/lifestyle-related**

**DODA prior weight → 0.2**

---

## 17. Sex — Weight = 0.2

`Sex` is a demographic variable.

Although sex-related differences can exist in diabetes prevalence and risk profiles, it is not assigned a high prior weight in this framework because it is not being used as a direct measure of a major modifiable diabetes risk factor.

**Clinical relevance → demographic/contextual**

**DODA prior weight → 0.2**

---

## 18. Healthcare Access Variables — Weight = 0.2

The following variables:

- `AnyHealthcare`
- `NoDocbcCost`

primarily represent access to or utilization of healthcare.

They may influence disease detection, prevention, and management, but they are not direct biological diabetes predictors.

Therefore, they are assigned the lowest prior-knowledge tier.

**Clinical relevance → contextual**

**DODA prior weight → 0.2**

---

# Summary of the Clinical Weighting Strategy

The clinical weighting strategy can therefore be summarized into four broad groups:

### Tier 1 — Very high prior clinical relevance

```text
BMI
HighBP
HeartDiseaseorAttack
Stroke
GenHlth
````

These variables receive a weight of `1.0`.

The first two are directly supported by established diabetes-risk evidence, while the latter variables represent important comorbidity or overall-health proxies.

### Tier 2 — High prior clinical relevance

```text
HighChol
Age
DiffWalk
PhysHlth
```

These variables receive weights between `0.8–0.9`.

### Tier 3 — Moderate prior clinical relevance

```text
MentHlth
Smoker
CholCheck
PhysActivity
```

These variables receive weights between `0.4–0.6`.

### Tier 4 — Low / contextual prior relevance

```text
Income
Education
Sex
Fruits
Veggies
HvyAlcoholConsump
AnyHealthcare
NoDocbcCost
```

These variables receive weights between `0.2–0.3`.

---

# Important Methodological Clarification

The numerical values in the JSON configuration should **not** be interpreted as:

* published ADA coefficients;
* relative risks;
* odds ratios;
* causal effects;
* regression coefficients;
* validated clinical prediction weights; or
* measures of the actual predictive importance of the features.

Instead, they represent **researcher-defined normalized prior-knowledge scores**.

The purpose of these scores is to provide DODA with a clinically informed prior that can be fused with statistical feature-selection scores.

---

# Limitations of the Clinical Weighting

Several limitations should be acknowledged.

### 1. Numerical weights are researcher-defined

There is no authoritative clinical table assigning values such as `BMI = 1.0` or `Sex = 0.2`.

The numerical mapping from clinical relevance to a 0–1 scale is therefore an operational design choice.

### 2. Some variables are proxies

Variables such as:

```text
GenHlth
PhysHlth
DiffWalk
Income
Education
AnyHealthcare
NoDocbcCost
```

are not direct biological diabetes-risk measurements.

Their weights represent contextual or clinical relevance rather than direct disease mechanisms.

### 3. BRFSS variables are simplified representations

Several variables are binary or self-reported.

For example, `PhysActivity` does not fully represent exercise frequency, duration, intensity, or sedentary behavior.

Similarly, `HighChol` does not provide the complete lipid profile.

### 4. The weights are not causal estimates

A high DODA clinical weight does not imply that the feature causes diabetes or that changing the feature would produce a proportional change in diabetes risk.

### 5. Clinical validation is still desirable

The weighting scheme should ideally be reviewed by a clinician, epidemiologist, or other domain expert before being presented as clinically validated prior knowledge.

---

# Reproducibility Statement

The exact clinical-weight configuration used in the reported experiments is:

```json
{
    "HighBP": 1.0,
    "HighChol": 0.9,
    "BMI": 1.0,
    "GenHlth": 1.0,
    "PhysHlth": 0.8,
    "MentHlth": 0.5,
    "Age": 0.9,
    "HeartDiseaseorAttack": 1.0,
    "Stroke": 1.0,
    "DiffWalk": 0.9,
    "Smoker": 0.6,
    "Income": 0.3,
    "Education": 0.3,
    "Sex": 0.2,
    "Fruits": 0.2,
    "Veggies": 0.2,
    "HvyAlcoholConsump": 0.2,
    "AnyHealthcare": 0.2,
    "NoDocbcCost": 0.2,
    "CholCheck": 0.4,
    "PhysActivity": 0.4
}
```

This configuration should be treated as the **fixed clinical-prior configuration for the current reported experiment**.

Any future changes should create a new configuration/version and should not overwrite the weights associated with previously reported results.

---

# References

1. **American Diabetes Association Professional Practice Committee.**
   *2. Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2026.*
   **Diabetes Care. 2026;49(Suppl. 1):S27–S49.**

   This guideline provides the primary evidence for diabetes screening and risk factors, including overweight/obesity, cardiovascular disease, hypertension, dyslipidemia, physical inactivity, and age.

   Source: [https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926/2-Diagnosis-and-Classification-of-Diabetes](https://diabetesjournals.org/care/article/49/Supplement_1/S27/163926/2-Diagnosis-and-Classification-of-Diabetes)

2. **American Diabetes Association Professional Practice Committee.**
   *3. Prevention or Delay of Diabetes and Associated Comorbidities: Standards of Care in Diabetes—2026.*
   **Diabetes Care. 2026;49(Suppl. 1):S50–S59.**

   This section provides evidence concerning prevention of type 2 diabetes, obesity/weight management, cardiovascular risk, hypertension, dyslipidemia, and physical activity.

   Source: [https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)

3. **American Diabetes Association Professional Practice Committee.**
   *5. Facilitating Positive Health Behaviors and Well-being to Improve Health Outcomes: Standards of Care in Diabetes—2026.*
   **Diabetes Care. 2026;49(Suppl. 1).**

   This section provides evidence and recommendations concerning physical activity and sedentary behavior among people with diabetes and those at risk for diabetes.

   Source: [https://diabetesjournals.org/care/article/49/Supplement_1/S89/163932/5-Facilitating-Positive-Health-Behaviors-and-Well](https://diabetesjournals.org/care/article/49/Supplement_1/S89/163932/5-Facilitating-Positive-Health-Behaviors-and-Well)

4. **American Diabetes Association Professional Practice Committee.**
   *10. Cardiovascular Disease and Risk Management: Standards of Care in Diabetes—2026.*
   **Diabetes Care. 2026;49(Suppl. 1):S216–S250.**

   This section provides supporting evidence concerning cardiovascular disease, stroke, hypertension, dyslipidemia, and cardiovascular risk in the context of diabetes.

   Source: [https://diabetesjournals.org/care/article/49/Supplement_1/S216/163933/10-Cardiovascular-Disease-and-Risk-Management](https://diabetesjournals.org/care/article/49/Supplement_1/S216/163933/10-Cardiovascular-Disease-and-Risk-Management)

---

# Status

**DRAFT — evidence-informed prior-knowledge mapping.**

The current numerical weights are **researcher-defined normalized clinical-prior scores**, not published clinical coefficients.

The strongest evidence supports the clinical relevance of variables such as:

* `BMI`
* `HighBP`
* `Age`
* `HighChol`
* `HeartDiseaseorAttack`
* `PhysActivity`

Other variables are incorporated as clinical, functional, socioeconomic, or healthcare-access proxies.

The weighting configuration is retained unchanged for the current experiment to preserve **experimental reproducibility and avoid post-hoc adjustment of clinical priors based on observed model performance**.

Future revisions to the weighting scheme should be versioned separately, documented in `CHANGELOG.md`, and evaluated as a new experimental configuration.

