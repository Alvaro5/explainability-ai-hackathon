# Executive Summary — HR Trusted AI

Hackathon IA x RH — Capgemini x ESILV | March 2026  
Team: Alvaro Serero, Ziyad Briand, Omar Bari, Le-Nguyen Nguyen, Rithiga Vengadessane

---

## The Problem

A fictional company is experiencing a high employee resignation rate and does not have a clear picture of who is at risk of leaving or why. HR managers need actionable insights, but existing data is scattered across HR records and no predictive tool is in place. At the same time, any AI solution deployed in an HR context carries real risks: biased predictions, opaque decisions, and sensitive personal data that must be handled carefully.

## Our Solution

We built an end-to-end AI pipeline that predicts which employees are at risk of leaving and explains the key factors behind each prediction in plain language. The solution is designed for HR managers with no technical background — the output is not just a score, it is an explanation they can act on.

The pipeline covers data anonymization, model training, SHAP-based explainability, and an interactive dashboard. The solution runs on a standard laptop and is also publicly deployed on Streamlit Community Cloud at https://explainability-ai-hackathon.streamlit.app/.

## Trusted AI Themes

We addressed two of the four hackathon themes.

**Explainable AI.** Every prediction comes with a per-employee explanation generated using SHAP values. HR managers can see not just that an employee is flagged as high risk, but which factors are driving that assessment — for example, a low pay rate combined with a short tenure. Global feature importance is also available to give HR teams a company-wide view of the main attrition drivers.

**Frugal AI.** We compared three models — Logistic Regression, Random Forest, and XGBoost — on both predictive performance and environmental cost measured with CodeCarbon. Logistic Regression was selected because it achieves an excellent F1 score (0.988) and ROC-AUC (1.000) while being lightweight, fast, and intrinsically interpretable. The total carbon footprint of the full training run is under 0.004g CO2eq, which is negligible. The solution deliberately avoids heavy infrastructure and oversized models.

## Results

| Model | ROC-AUC | F1 Score | CO2 Emissions |
|---|---|---|---|
| Logistic Regression (selected) | 1.000 | 0.988 | 0.0020g |
| Random Forest | 1.000 | 0.994 | 0.0011g |
| XGBoost | 0.994 | 0.988 | 0.0001g |

Metrics are from 5-fold cross-validation on a synthetic dataset of approximately 400 employee records.

## Responsible AI

The solution was built with compliance in mind from the start. Personal data is anonymized before any processing using suppression, pseudonymization, and generalization techniques. Sensitive attributes (gender, ethnicity) are never fed into the model — they are kept in a separate file used only for bias auditing. Under the EU AI Act, this type of system falls under High Risk (employment context), which means human oversight is required before any HR decision is made based on the model's output. This is enforced by design in the dashboard.

## Deliverables

The GitHub repository contains three notebooks covering data processing, model training with explainability, and the frugal comparison; a Streamlit dashboard with five pages (Dashboard, Employee Profile, HR Analysis, AI Approach, Compliance & Ethics); a model card and data card; and this document. Everything is documented and reproducible.

- **Repository**: https://github.com/Alvaro5/explainability-ai-hackathon
- **Live dashboard**: https://explainability-ai-hackathon.streamlit.app/
