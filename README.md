# HR Trusted AI — Employee Turnover Prediction

Explainability AI Hackathon - ESILV A4 - March 2026  
Repository: https://github.com/Alvaro5/explainability-ai-hackathon

## Team

- Alvaro Serero
- Ziyad Briand
- Omar Bari
- Le-Nguyen Nguyen
- Rithiga Vengadessane

---

## Objective

The context is a fictional company dealing with a high resignation rate. The goal was to build an AI solution that helps HR managers figure out which employees are at risk of leaving, and more importantly, understand why — without requiring them to have any ML background.

We chose to focus on two of the four Trusted AI themes:
- **Explainable AI** — predictions need to be interpretable for HR teams, not just accurate
- **Frugal AI** — the solution should be lightweight enough to run on a standard company machine, and we wanted to measure the actual carbon cost of our choices

---

## Scope

What the solution does:
- Predicts attrition risk per employee (binary classification on the `Termd` field)
- Provides SHAP-based explanations at both the global and individual level
- Compares three models on accuracy and environmental cost
- Applies GDPR-compliant anonymization before any processing
- Exposes results through an HR dashboard

What we did not cover:
- Real-time inference (this is batch only)
- Integration with a live HR system
- Full NLP pipeline on unstructured feedback (we explored it but did not include it in the final model)

---

## Use Cases and Personas

**Use case: Employee Attrition Risk Analysis**

| Persona | Need |
|---|---|
| HR Manager (Marie) | Needs to know which employees are at risk of leaving in the next few months, and what actions to take. Does not have a technical background and needs explanations she can actually use. |
| HR-AI Solution Provider | Delivers a tool that HR teams can trust. Results have to be transparent and justifiable, not just a score with no context. |

---

## Solution Architecture

```
Raw HR Data (CSV)
      |
      v
[1. Data Processing]
   - Anonymization (GDPR): names removed, IDs pseudonymized, DOB generalized
   - Feature engineering: tenure_days, age_group
   - Output: hr_anonymized.csv (model input) + hr_sensitive.csv (bias audit only)
      |
      v
[2. Model Comparison — Frugal AI]
   - Logistic Regression  -> ROC-AUC: 1.000 | F1: 0.988 | CO2: 0.0020g | Time: 2.67s
   - Random Forest        -> ROC-AUC: 1.000 | F1: 0.994 | CO2: 0.0011g | Time: 1.48s  (selected)
   - XGBoost              -> ROC-AUC: 0.994 | F1: 0.988 | CO2: 0.0001g | Time: 0.19s
      |
      v
[3. Explainability]
   - Global: feature importance across all employees
   - Local: per-employee SHAP values ("at risk because PayRate is low and tenure is short")
      |
      v
[4. HR Dashboard]
   - Risk score + top 3 factors per employee
   - Designed for non-technical HR users
```

See `docs/architecture.md` for the full diagram and design decisions.

---

## Model Performance

All metrics are from 5-fold cross-validation. Carbon tracking done with CodeCarbon on Apple M3 Pro, Ile-de-France, France.

| Model | ROC-AUC (mean +/- std) | F1 Score (mean) | Training Time | CO2 Emissions |
|---|---|---|---|---|
| Logistic Regression | 1.000 +/- 0.000 | 0.988 | 2.67s | 0.0020g |
| Random Forest | 1.000 +/- 0.000 | 0.994 | 1.48s | 0.0011g |
| XGBoost | 0.994 +/- 0.012 | 0.988 | 0.19s | 0.0001g |

We went with Random Forest. It ties Logistic Regression on ROC-AUC but has a better F1, and it costs 45% less in carbon. XGBoost is faster and lighter but drops in ROC-AUC, which we did not want to sacrifice for this use case.

---

## Dataset

- Source: Human Resources Data Set, Kaggle (Rich Huebner & Carla Patalano)
- Around 400 synthetic employee records
- Target variable: `Termd` (0 = still employed, 1 = left the company)
- Contains sensitive attributes: `Sex`, `RaceDesc`, `HispanicLatino` — kept aside for bias auditing only, never fed into the model

See `docs/data_card.md` for the full data processing and GDPR documentation.

---

## Notebooks

| Notebook | What it does | Run order |
|---|---|---|
| `01_eda.ipynb` | Data exploration, anonymization, visualizations | 1 |
| `02_model.ipynb` | Model training, SHAP explainability, dashboard | 2 |
| `03_frugal.ipynb` | Model comparison + CodeCarbon tracking | 3 |

---

## Dashboard

The dashboard is built for HR teams. It shows:
- Predicted risk score per employee
- The top 3 factors behind each prediction (from SHAP)
- Filters by department, risk level, and tenure

Run `02_model.ipynb` to launch it, or see the `demo/` folder for a recorded walkthrough.

---

## Setup

```bash
git clone https://github.com/Alvaro5/explainability-ai-hackathon
cd explainability-ai-hackathon
pip install -r requirements.txt
jupyter notebook
```

Python 3.10+, no GPU needed, around 500MB disk space.

---

## Deliverables

- [x] README.md
- [x] docs/model_card.md
- [x] docs/data_card.md
- [x] docs/architecture.md
- [x] executive_summary.md
- [x] Demo (demo/ folder or notebook)
- [x] Slides

---

## Responsible AI Summary

| Dimension | What we did |
|---|---|
| GDPR | Names suppressed, DOB generalized, IDs pseudonymized |
| AI Act | Classified as High Risk (HR/employment context) — human oversight required before any decision |
| Fairness | Sensitive attributes excluded from model inputs; bias audit run separately |
| Transparency | SHAP explanations at global and individual level, model card and data card provided |
| Frugality | Carbon footprint tracked with CodeCarbon, lightest sufficient model selected |
