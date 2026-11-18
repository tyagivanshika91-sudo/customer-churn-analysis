-- Run these queries against outputs/customer_churn.sqlite
-- The Python analysis script creates a SQLite table named customers.

-- 1. Overall churn and retention
SELECT
    COUNT(*) AS total_customers,
    SUM(Churn_Flag) AS churned_customers,
    COUNT(*) - SUM(Churn_Flag) AS retained_customers,
    ROUND(100.0 * SUM(Churn_Flag) / COUNT(*), 2) AS churn_rate_pct
FROM customers;

-- 2. Churn by contract type
SELECT
    Contract,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * AVG(Churn_Flag), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 3. Churn by payment method
SELECT
    PaymentMethod,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * AVG(Churn_Flag), 2) AS churn_rate_pct
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;

-- 4. Churn by tenure group
SELECT
    Tenure_Group,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * AVG(Churn_Flag), 2) AS churn_rate_pct
FROM customers
GROUP BY Tenure_Group
ORDER BY churn_rate_pct DESC;

-- 5. Average monthly charges: churned vs retained
SELECT
    Churn,
    COUNT(*) AS customers,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(tenure), 1) AS avg_tenure_months
FROM customers
GROUP BY Churn;
