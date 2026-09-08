# Clinical Feature Weights — UCI Heart Disease

## Purpose

These weights are designed for the DODA clinical-weighting component for the UCI Heart Disease (Cleveland) dataset.

The weights represent **relative clinical importance**, not probabilities, regression coefficients, or official guideline-derived numerical risk scores. They are intended to provide a transparent ordinal prior that can be combined with statistical feature-selection scores.

## Reference basis

The weighting rationale is based on two sources:

1. **American Heart Association (AHA)** information on coronary artery disease and cardiovascular risk, which identifies factors such as increasing age, sex, high blood pressure, high cholesterol, diabetes, overweight/obesity, and tobacco use as important cardiovascular risk factors.
2. **UCI Heart Disease dataset documentation**, which defines the clinical meaning of the Cleveland variables, including chest-pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, maximum heart rate, exercise-induced angina, ST depression, ST-segment slope, number of major vessels, and thalassemia-related findings.

The UCI target represents angiographic heart-disease status, where the original target distinguishes absence from presence of disease.

## Weighting scale

| Weight | Interpretation |
|---:|---|
| 1.0 | Very high clinical relevance / direct diagnostic evidence |
| 0.9 | High clinical relevance |
| 0.8 | Moderately high clinical relevance |
| 0.6 | Moderate clinical relevance |
| 0.2–0.5 | Lower clinical relevance |

## Feature-level rationale

### 1. `age` — 0.9

Increasing age is an established cardiovascular risk factor. The AHA identifies increasing age as an important risk factor for heart attack and coronary artery disease. Therefore, age receives a high weight, although it is not itself a diagnostic finding.

### 2. `sex` — 0.6

Sex is associated with differences in cardiovascular risk and timing of disease. However, it is a demographic characteristic rather than a direct clinical measurement of coronary disease, so it receives a moderate weight.

### 3. `cp` — 1.0

Chest-pain type is directly related to the clinical presentation of coronary disease. The UCI dataset defines categories including typical angina, atypical angina, non-anginal pain, and asymptomatic presentation. Because it is a clinically informative symptom variable, it receives a very high weight.

### 4. `trestbps` — 0.9

Resting blood pressure is strongly relevant to cardiovascular disease. High blood pressure is an established cardiovascular risk factor and can contribute to arterial damage and coronary disease. It therefore receives a high weight.

### 5. `chol` — 0.8

Cholesterol is an established cardiovascular risk factor, particularly through abnormal LDL cholesterol. The UCI variable is total serum cholesterol rather than LDL specifically, so it receives a moderately high rather than maximum weight.

### 6. `fbs` — 0.6

The variable indicates whether fasting blood sugar is greater than 120 mg/dL. Abnormal glucose regulation and diabetes are important cardiovascular risk factors, but this binary threshold is a relatively limited representation of metabolic risk. Therefore, it receives a moderate weight.

### 7. `restecg` — 0.8

Resting ECG abnormalities can provide clinically relevant information about cardiac electrical activity and structural abnormalities. Since it is a clinical examination measure but not a direct angiographic measure of coronary obstruction, it receives a moderately high weight.

### 8. `thalach` — 0.8

Maximum heart rate achieved during exercise is an exercise-test measure and can provide clinically relevant information about cardiovascular functional response. It receives a moderately high weight.

### 9. `exang` — 1.0

Exercise-induced angina is directly related to exertional myocardial ischemia and is therefore highly informative clinically. It receives a very high weight.

### 10. `oldpeak` — 1.0

Oldpeak represents ST-segment depression induced by exercise relative to rest. Exercise-induced ST depression is a clinically important indicator of myocardial ischemia, so it receives a very high weight.

### 11. `slope` — 0.9

The slope of the peak exercise ST segment is part of the exercise ECG assessment and provides clinically relevant information about ischemic response. It therefore receives a high weight.

### 12. `ca` — 1.0

The UCI dataset defines `ca` as the number of major vessels (0–3) colored by fluoroscopy. This is a direct anatomical/angiographic measure associated with coronary vessel involvement and is therefore assigned maximum clinical weight.

### 13. `thal` — 1.0

The UCI dataset defines `thal` using thalassemia-related findings, including normal, fixed defect, and reversible defect categories. It is a clinically informative cardiac test finding and receives maximum weight in this framework.

## Final weights

```json
{
    "age": 0.9,
    "sex": 0.6,
    "cp": 1.0,
    "trestbps": 0.9,
    "chol": 0.8,
    "fbs": 0.6,
    "restecg": 0.8,
    "thalach": 0.8,
    "exang": 1.0,
    "oldpeak": 1.0,
    "slope": 0.9,
    "ca": 1.0,
    "thal": 1.0
}
```

## Important methodological note

These values are **analyst-defined ordinal clinical weights** constructed from the cited clinical evidence and the meaning of the UCI variables. They should not be described as official AHA weights or as validated clinical risk coefficients.

For the DODA experiment, the weights should be applied consistently across the statistical feature-selection methods and should be kept independent of the observed target correlations. This prevents the clinical-weighting component from simply reproducing information already present in the dataset.

### Sources

- American Heart Association. *Coronary Artery Disease — Coronary Heart Disease*. https://www.heart.org/en/health-topics/consumer-healthcare/what-is-cardiovascular-disease/coronary-artery-disease
- American Heart Association. *Understand Your Risks to Prevent a Heart Attack*. https://www.heart.org/en/health-topics/heart-attack/understand-your-risks-to-prevent-a-heart-attack
- UCI Machine Learning Repository. *Heart Disease Dataset*. https://archive.ics.uci.edu/dataset/45/heart%2Bdisease
