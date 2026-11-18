# Data Dictionary

The IBM Telco Customer Churn sample contains one row per customer.

| Field | Meaning |
|---|---|
| customerID | Unique customer identifier |
| gender | Customer gender category |
| SeniorCitizen | 1 indicates senior citizen; 0 otherwise |
| Partner | Whether customer has a partner |
| Dependents | Whether customer has dependents |
| tenure | Number of months with the company |
| PhoneService | Whether phone service is active |
| MultipleLines | Multiple-line service status |
| InternetService | DSL, Fiber optic, or no internet service |
| OnlineSecurity | Online security add-on status |
| OnlineBackup | Online backup add-on status |
| DeviceProtection | Device protection add-on status |
| TechSupport | Tech support add-on status |
| StreamingTV | Streaming TV add-on status |
| StreamingMovies | Streaming movies add-on status |
| Contract | Month-to-month, one-year, or two-year contract |
| PaperlessBilling | Whether paperless billing is enabled |
| PaymentMethod | Customer payment method |
| MonthlyCharges | Current monthly charge (USD) |
| TotalCharges | Total charges to date (USD) |
| Churn | Yes if customer left within the last month; otherwise No |
| Churn_Flag | Derived field: Yes=1, No=0 |
| Tenure_Group | Derived tenure band used for segmentation |

## Data-quality note
`TotalCharges` is stored as text in the raw file. Eleven rows have blank values corresponding to zero-tenure customers. The analysis script converts the field to numeric and fills these blank cumulative charges with 0 while retaining the customer records.
