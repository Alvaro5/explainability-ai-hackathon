# HR Trusted AI - Employee Turnover Prediction
Hackathon Explainability AI - ESILV A4 - March 2026

## Team :
```bash
Alvaro Serero
Ziyad Briand
Omar Bari
Le-Nguyen Nguyen
Rithiga Vengadessane
```

## Objective

An imaginary company is facing a high resignation rate. The goal of this project is to build an AI solution that helps HR teams identify employees who may leave and understand the main reasons behind it. The approach focuses on transparency and efficiency.

The project is based on two main ideas:
- making the model understandable for non-technical users
- keeping the solution lightweight in terms of resources

These two directions were chosen because HR use cases require both trust and practicality. The predictions made by the model can impact important decisions, so they must be understandable and justified. At the same time, the solution needs to be simple enough to be deployed in a real company environment without requiring heavy infrastructure.

Explainable AI is used to ensure that HR managers can understand the results produced by the model. Instead of providing only a risk score, the model also gives clear explanations for each prediction. We use methods such as feature importance and SHAP values to show which variables have the most influence. This allows HR teams to understand why an employee is considered at risk, for example due to low satisfaction, high overtime, or salary level.

Frugal AI focuses on building a solution that remains efficient while using limited resources. Instead of directly relying on complex models, we compare several approaches such as logistic regression, random forest, and more advanced methods. We evaluate both their performance and their computational cost. The objective is to select a model that provides good results while remaining simple, efficient, and easy to use in practice.

## Use Cases & Personas

### Use Case: Employee Attrition Risk Analysis

| Persona | Need |
|---|---|
| HR Manager (Marie) | Needs to identify employees at risk of leaving and understand what actions to take |
| HR-AI Solution Provider | Provides a tool that helps HR teams make decisions based on clear and understandable results |

## Solution Architecture

1. Raw HR Data (CSV)  
2. Data Processing (cleaning, anonymization, feature engineering)  
3. Model (Logistic Regression, Random Forest, XGBoost comparison)  
4. Explainability (feature importance, SHAP analysis)  
5. Dashboard (risk score and explanation for each employee)


## Dataset

- Source: Human Resources Data Set and Kaggle (Rich Huebner)
- Around 400 synthetic employee records
- Target variable: Termd (0 = still employed, 1 = left the company)
- Includes sensitive attributes such as gender and ethnicity

## Notebooks

| Notebook | Description |
|---|---|
| 01_eda.ipynb | Data exploration and preparation |
| 02_model.ipynb | Model training and explanations |
| 03_frugal.ipynb | Model comparison and efficiency analysis |

## Dashboard

We built a dashboard designed for HR teams to explore employee data and identify potential risks of departure.

The dashboard allows users to:
- view the predicted risk score for each employee
- understand the main factors influencing the prediction
- explore key indicators such as satisfaction, salary, and performance

This tool helps HR managers make informed decisions and take preventive actions based on clear and accessible insights.

## Deliverables

- README.md
- docs/model_card.md
- docs/data_card.md
- docs/architecture.md
- executive_summary.md
- demo of the solution
- slides

## Setup

```bash
git clone https://github.com/YOUR_TEAM/hr-trusted-ai
cd hr-trusted-ai
pip install -r requirements.txt
jupyter notebook


Explainability :

The model is designed to provide clear explanations for its predictions. For each employee, it is possible to identify the main factors that influence the risk of leaving.

Two types of explanations are used:

Overall feature importance and individual explanations for each prediction.


Frugality :

Several models are compared in terms of performance and resource usage:

Logistic Regression, Random Forest and XGBoost.

The goal is to choose a model that gives good results while remaining efficient.
