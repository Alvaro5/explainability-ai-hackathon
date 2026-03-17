# Data Card — HR Dataset

## Overview

| Field | Detail |
|---|---|
| Source | Kaggle — Human Resources Data Set (Rich Huebner & Carla Patalano) |
| Size | ~400 synthetic employee records |
| Training split | ~310 training / ~90 test (80/20, stratified by target) |
| Target variable | `Termd` (0 = active, 1 = terminated or resigned) |
| Class balance | Imbalanced — majority is Termd=0, handled with stratified sampling |
| Nature | Fully synthetic, created for an academic HR analytics case study |

---

## Sensitive Attributes

The dataset contains several attributes that are sensitive under GDPR and relevant for fairness auditing. We handled them differently depending on their role.

| Attribute | Why it is sensitive | What we did |
|---|---|---|
| Employee Name | Direct personal identifier | Removed entirely |
| Sex | Protected characteristic | Kept in a separate file for bias audit only — not used in model |
| RaceDesc | Protected characteristic | Kept in a separate file for bias audit only — not used in model |
| HispanicLatino | Protected characteristic | Kept in a separate file for bias audit only — not used in model |
| DOB | Personal data (age derivable) | Replaced with age_group (decade buckets) |
| Zip, State | Location data | Removed entirely |
| DateofHire, DateofTermination | Personal data with temporal patterns | Converted to tenure_days, raw dates not retained |

---

## GDPR Compliance

We applied four standard anonymization techniques:

**Suppression** — fields that could directly re-identify someone (name, email, zip, state) were removed before any analysis.

**Pseudonymization** — EmpID was kept as an anonymous key so records can be tracked internally without any linkable personal data attached.

**Generalization** — date of birth was converted to an age group (20s, 30s, 40s, 50s+) to remove exact age while keeping the demographic signal useful for analysis.

**Aggregation** — hire and termination dates were converted to a single numeric field (tenure_days). No raw dates appear in the processed files.

Legal basis for processing: legitimate interest in workforce analytics. Data is not shared externally. Sensitive attributes are only used for fairness auditing within the project and never enter the prediction model.

---

## Processing Pipeline

```
raw/HRDataset.csv
      |
      v  Suppression       -> Remove: Employee Name, Email, Zip, State
      v  Pseudonymization  -> Keep EmpID as anonymous key only
      v  Generalization    -> DOB -> age_group (decade bucket)
      v  Aggregation       -> DateofHire + DateofTermination -> tenure_days
      v  Encoding          -> Categorical variables to numeric
      v  Split on sensitivity
      |
      |-- processed/hr_anonymized.csv   <- used for model training and inference
      |-- processed/hr_sensitive.csv    <- used only for bias audit, never enters model
```

---

## Feature Engineering

| Feature | Source columns | Description |
|---|---|---|
| `tenure_days` | DateofHire, DateofTermination or reference date | Number of days employed at time of prediction |
| `age_group` | DOB | Decade bucket: 20s, 30s, 40s, 50s+ |

---

## Known Limitations

- The data is synthetic, so attrition patterns may not match what you would see in a real company. Performance numbers look strong partly because of this.
- There is class imbalance (most employees are still active). We handled this with stratified splitting but a more robust approach on a larger dataset would use resampling or class weighting.
- Some fields like ManagerID have a lot of missing values and were excluded from the model.
- DateofTermination was excluded from features to avoid target leakage — it is only available for employees who have already left, which would make the prediction trivial.
- The Sex field only contains M and F. Non-binary identities are not represented, which limits the scope of the gender bias audit.
