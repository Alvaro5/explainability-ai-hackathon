# Model Card — HR Attrition Prediction

## Overview

| Field | Detail |
|---|---|
| Task | Binary classification — predict employee attrition (`Termd`: 0 = active, 1 = terminated) |
| Selected model | Random Forest |
| Baseline | Logistic Regression |
| XAI method | SHAP (SHapley Additive exPlanations) |
| Carbon tracking | CodeCarbon v3.2.3 |
| Hardware | Apple M3 Pro, 12 cores, 18GB RAM — Ile-de-France, France |

---

## Why This Model?

We tried three models and measured both predictive performance and resource cost. The idea was not to go straight for the most powerful option, but to find the one that gives good enough results at the lowest cost — which is what frugal AI is about.

| Model | ROC-AUC (CV mean +/- std) | F1 Score (CV mean) | Training Time | CO2 Emissions |
|---|---|---|---|---|
| Logistic Regression | 1.000 +/- 0.000 | 0.988 | 2.67s | 0.0020g |
| Random Forest | 1.000 +/- 0.000 | 0.994 | 1.48s | 0.0011g |
| XGBoost | 0.994 +/- 0.012 | 0.988 | 0.19s | 0.0001g |

We picked Random Forest. It matches Logistic Regression on ROC-AUC but gets a higher F1 (0.994 vs 0.988), and it is actually cheaper — 45% less CO2 and faster to train. XGBoost is the lightest option but it loses 0.006 on ROC-AUC compared to the other two, which we did not want to accept for a use case where false negatives have real consequences (missing an at-risk employee).

We set a rule before running the comparison: only choose XGBoost if it has a F1 gain of more than 5 percentage points over the others. It does not, so it stays as a reference point.

Full emissions data is in `emissions.csv`.

### Why Random Forest works well for explainability

Random Forest fits well with SHAP because it produces stable feature importances across trees, which makes the local explanations more reliable. With Logistic Regression, SHAP explanations are essentially just the coefficients, which is less informative for HR users. With XGBoost the explanations are noisier on a small dataset.

---

## Input Features

| Feature | Type | Description |
|---|---|---|
| `PayRate` | Float | Hourly pay rate |
| `PerfScoreID` | Integer | Performance score (1 to 4) |
| `EmpStatusID` | Integer | Employment status code |
| `DeptID` | Integer | Department identifier |
| `MarriedID` | Binary | Marital status |
| `FromDiversityJobFairID` | Binary | Whether the employee was sourced from a diversity job fair |
| `tenure_days` | Integer | Days between hire date and the reference date |

Note: sensitive attributes (`Sex`, `RaceDesc`, `HispanicLatino`) are not in this list. They are stored separately and only used to audit the model for bias after training — they never go into the model.

---

## Output

| Output | Description |
|---|---|
| `attrition_risk` | Probability score between 0 and 1 |
| `risk_label` | Low (below 0.3), Medium (0.3 to 0.6), High (above 0.6) |
| `top_factors` | Top 3 SHAP features driving this employee's prediction |

---

## Limitations

- The model is trained on synthetic data with around 310 training samples. Performance numbers look very good but this is partly because the dataset is synthetic and relatively clean. Results on real company data would likely be lower.
- The dataset is small, so there is variance risk. We used 5-fold cross-validation to get a more reliable estimate but a larger dataset would give more confidence.
- The model reflects one fictional company's attrition patterns. It may not generalize to organizations with different compensation structures or HR cultures.
- SHAP values are locally faithful approximations. For employees near the decision boundary (score around 0.5), the explanation may simplify complex interactions between features.
- The model should never be the sole basis for an HR decision. It is a tool to support judgment, not replace it.

---

## AI Act Risk Level

This kind of system falls under High Risk in the EU AI Act (Annex III, employment and worker management). That means:

| Requirement | Status |
|---|---|
| Human oversight before any decision based on the model | Required — documented in the dashboard |
| Logging and auditability of predictions | Implemented |
| Explanation available to affected employees on request | Covered by SHAP outputs |
| Technical documentation | This model card + data card |
| Bias and fairness audit | Done on hr_sensitive.csv, separate from model inputs |
