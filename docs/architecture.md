# Architecture — HR Trusted AI

## Overview

The solution is split into four sequential stages: data preparation, model training, explainability, and a dashboard for HR users. Each stage feeds into the next, and the whole pipeline can be reproduced by running the three notebooks in order.

---

## Full Pipeline

```
+---------------------------+
|   raw/HRDataset.csv       |
|   (~400 employee records) |
+---------------------------+
             |
             v
+----------------------------------+
|   1. Data Processing             |
|   notebook: 01_eda.ipynb         |
|                                  |
|   - Remove PII (name, zip, etc.) |
|   - Pseudonymize EmpID           |
|   - Generalize DOB -> age_group  |
|   - Compute tenure_days          |
|   - Encode categoricals          |
|   - Split sensitive attributes   |
+----------------------------------+
        |               |
        v               v
hr_anonymized.csv   hr_sensitive.csv
(model input)       (bias audit only)
        |
        v
+------------------------------------------+
|   2. Model Training — Frugal AI          |
|   notebook: 03_frugal.ipynb              |
|                                          |
|   Three models compared:                 |
|   - Logistic Regression (baseline)       |
|   - Random Forest        (selected)      |
|   - XGBoost              (reference)     |
|                                          |
|   Metrics: ROC-AUC, F1 (5-fold CV)       |
|   Carbon: tracked with CodeCarbon        |
|   Output: emissions.csv,                 |
|           frugal_comparison.csv          |
+------------------------------------------+
             |
             v
+------------------------------------------+
|   3. Explainability — XAI                |
|   notebook: 02_model.ipynb               |
|                                          |
|   - Global: feature importance plot      |
|   - Local: per-employee SHAP waterfall   |
|   - Output: risk score + top 3 factors   |
|     per employee in plain language       |
+------------------------------------------+
             |
             v
+------------------------------------------+
|   4. HR Dashboard (Streamlit)            |
|   app: app.py + model.py                 |
|                                          |
|   Pages:                                 |
|   - Dashboard: KPIs, at-risk table       |
|   - Employee Profile: individual SHAP    |
|   - HR Analysis: company-wide analytics  |
|   - AI Approach: model & SHAP docs       |
|   - Compliance & Ethics: GDPR, AI Act    |
|                                          |
|   Deployed: Streamlit Community Cloud    |
+------------------------------------------+
```

---

## Design Decisions

### Why we separated hr_sensitive.csv from hr_anonymized.csv

Keeping sensitive attributes (Sex, RaceDesc, HispanicLatino) in the model input file would have been the easiest path, but it creates two problems. First, it means the model could be using protected characteristics to make predictions, which is exactly what we want to avoid. Second, it makes GDPR compliance harder to argue.

By splitting the data early in the pipeline, we make it structurally impossible for the model to use these attributes. The sensitive file only gets loaded in the bias audit step, where we check whether the model's outputs are fair across demographic groups — but the model itself never sees them during training.

### Why Random Forest over Logistic Regression and XGBoost

See `docs/model_card.md` for the full comparison. The short version: Random Forest matches Logistic Regression on ROC-AUC, gets a higher F1, and is actually cheaper in terms of CO2 and training time. XGBoost is the lightest option but has slightly lower ROC-AUC, which matters in a high-risk HR context.

### Why SHAP over LIME or other methods

SHAP gives consistent global and local explanations from the same framework, which made it easier to build a coherent dashboard. With Random Forest on a small dataset, SHAP values are also more stable than LIME approximations. The main tradeoff is that SHAP is slower to compute, but on 400 records this is not an issue.

### Batch inference, not real-time

The solution runs as a batch job rather than a real-time API. This fits the use case — HR teams do not need a live prediction for every action, they need a periodic analysis (e.g. monthly) that they can review and act on. Batch inference also keeps the infrastructure requirements minimal, which is consistent with the frugal AI approach.

---

## File Structure

```
explainability-ai-hackathon/
|
|-- raw/
|   |-- HRDataset.csv
|
|-- processed/
|   |-- hr_anonymized.csv
|   |-- hr_sensitive.csv
|
|-- 01_eda.ipynb
|-- 02_model.ipynb
|-- 03_frugal.ipynb
|
|-- app.py                    <- Streamlit entry point
|-- model.py                  <- data loading, feature engineering, model training
|-- pages_employees.py        <- Employee Profile page
|-- pages_analysis.py         <- HR Analysis page
|-- pages_ia.py               <- AI Approach + Compliance & Ethics pages
|
|-- .streamlit/
|   |-- config.toml           <- dark theme configuration
|
|-- emissions.csv
|-- frugal_comparison.csv
|-- frugal_comparison.png
|
|-- docs/
|   |-- architecture.md       <- this file
|   |-- model_card.md
|   |-- data_card.md
|
|-- executive_summary.md
|-- README.md
|-- requirements.txt
|-- .gitignore
```

---

## Reproduction

Run the notebooks in this order:

1. `01_eda.ipynb` — produces `processed/hr_anonymized.csv` and `processed/hr_sensitive.csv`
2. `03_frugal.ipynb` — runs the model comparison and produces `emissions.csv` and `frugal_comparison.csv`
3. `02_model.ipynb` — trains the final Random Forest, generates SHAP explanations, and launches the dashboard

Each notebook is self-contained and includes comments explaining each step. No GPU is required. The full pipeline runs in under 10 seconds on a standard laptop.

---

## Dashboard Deployment

The Streamlit dashboard is deployed on **Streamlit Community Cloud**:

- **URL**: https://explainability-ai-hackathon.streamlit.app/
- **Platform**: Streamlit Community Cloud (free tier)
- **Auto-deploy**: pushes to `main` trigger automatic redeployment
- **Entry point**: `app.py`
- **Theme**: dark mode via `.streamlit/config.toml`

To run locally: `streamlit run app.py` (opens at `http://localhost:8501`).
