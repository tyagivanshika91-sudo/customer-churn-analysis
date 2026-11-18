# Customer Churn Analysis

**Portfolio case study | Business Analytics**

## Business question
A fictional subscription-based telecommunications company wants to understand customer churn, identify customer segments with higher observed churn, and prioritize retention actions for further testing.

This is a descriptive business analysis, not a causal study or a deployed churn-prediction model.

## Dataset
- **Name:** IBM Telco Customer Churn sample dataset
- **Source repository:** https://github.com/IBM/telco-customer-churn-on-icp4d
- **Direct CSV:** https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv
- **Expected shape:** 7,043 customer records and 21 columns
- **Unit of analysis:** one customer record
- **Target:** `Churn` (Yes/No)

The original `TotalCharges` field is text-like and has 11 blank values associated with zero-tenure customers. The analysis script converts it to numeric and records the cleaning treatment. The raw dataset is downloaded locally and is not committed to GitHub.

## Project questions
1. What is the overall customer churn rate?
2. How does observed churn differ by contract type?
3. Which tenure groups have higher observed churn?
4. How does churn vary by internet service and payment method?
5. What customer-retention actions should management test?

## Tools
Python (pandas, matplotlib), Excel workbook export, SQLite, SQL.

## Run on Windows (VS Code terminal)
Open this folder in VS Code, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.download_data
python -m src.analyze_churn
```

If PowerShell blocks activation, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.download_data
.\.venv\Scripts\python.exe -m src.analyze_churn
```

## Outputs created after running
- `data/processed/telco_churn_clean.csv` — cleaned analysis data
- `outputs/churn_analysis.xlsx` — KPI and segment tables for Excel
- `outputs/kpi_summary.csv` — headline KPIs
- `outputs/churn_by_*.csv` — segment-level analysis tables
- `outputs/churn_overview.png` — chart for the report/dashboard
- `outputs/customer_churn.sqlite` — SQLite database
- `outputs/cleaning_log.txt` — data-cleaning notes

## Power BI dashboard plan
Use `data/processed/telco_churn_clean.csv` in Power BI Desktop.
Suggested cards: Total Customers, Churned Customers, Churn Rate, Retained Customers.
Suggested visuals: churn by Contract, churn by Tenure Group, churn by Internet Service, churn by Payment Method.
Add slicers for Contract, Internet Service, and Tenure Group.
Use the observed segment rates carefully: they are associations in this sample, not proof of causes.

## Repository structure
```text
customer-churn-analysis/
├── data/
│   ├── raw/                 # downloaded source file (gitignored)
│   └── processed/           # generated cleaned file (gitignored)
├── docs/
│   └── data_dictionary.md
├── outputs/                 # generated outputs (gitignored)
├── sql/
│   └── analysis_queries.sql
├── src/
│   ├── __init__.py
│   ├── download_data.py
│   └── analyze_churn.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Important limitations
- This is a sample dataset for learning and portfolio demonstration, not a live company's customer database.
- Segment differences are descriptive. They do not establish why a customer churned.
- Retention recommendations should be treated as hypotheses to test, not proven interventions.
- Do not claim a reduction in churn or revenue impact unless an intervention is actually tested and measured.
