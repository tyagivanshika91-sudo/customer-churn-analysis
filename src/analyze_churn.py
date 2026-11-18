from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

RAW = Path("data/raw/Telco-Customer-Churn.csv")
PROCESSED = Path("data/processed/telco_churn_clean.csv")
OUT = Path("outputs")
CHARTS = OUT / "charts"

def save_segment(df, column, filename):
    result = (
        df.groupby(column, dropna=False)
          .agg(customers=("customerID", "count"),
               churned=("Churn_Flag", "sum"),
               churn_rate=("Churn_Flag", "mean"),
               avg_monthly_charges=("MonthlyCharges", "mean"))
          .reset_index()
          .sort_values("churn_rate", ascending=False)
    )
    result["churn_rate"] = (result["churn_rate"] * 100).round(2)
    result["avg_monthly_charges"] = result["avg_monthly_charges"].round(2)
    result.to_csv(OUT / filename, index=False)
    return result

def main():
    if not RAW.exists():
        raise FileNotFoundError(
            "Raw dataset not found. First run: python -m src.download_data"
        )

    OUT.mkdir(parents=True, exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW)

    required = {"customerID", "tenure", "Contract", "InternetService",
                "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"}
    missing_cols = required - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing expected columns: {sorted(missing_cols)}")

    original_rows = len(df)
    duplicate_ids = int(df["customerID"].duplicated().sum())
    blank_total_before = int(df["TotalCharges"].astype(str).str.strip().eq("").sum())

    # TotalCharges is stored as text in the raw sample. Convert safely.
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    missing_total = int(df["TotalCharges"].isna().sum())
    zero_tenure_missing = int(((df["tenure"] == 0) & df["TotalCharges"].isna()).sum())

    # The blank TotalCharges rows are zero-tenure customers with no accumulated charges.
    # Keep these customer records and assign 0 to cumulative charges.
    df["TotalCharges"] = df["TotalCharges"].fillna(0)
    df["Churn_Flag"] = df["Churn"].map({"Yes": 1, "No": 0})
    if df["Churn_Flag"].isna().any():
        raise ValueError("Unexpected values found in Churn; inspect the raw dataset.")

    # Business-friendly tenure bands.
    df["Tenure_Group"] = pd.cut(
        df["tenure"],
        bins=[-1, 12, 24, 48, 72],
        labels=["0–12 months", "13–24 months", "25–48 months", "49–72 months"]
    )

    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED, index=False)

    total_customers = len(df)
    churned = int(df["Churn_Flag"].sum())
    retained = total_customers - churned
    churn_rate = churned / total_customers * 100
    avg_tenure_churned = df.loc[df["Churn_Flag"] == 1, "tenure"].mean()
    avg_tenure_retained = df.loc[df["Churn_Flag"] == 0, "tenure"].mean()
    monthly_charges_churned = df.loc[df["Churn_Flag"] == 1, "MonthlyCharges"].mean()
    monthly_charges_retained = df.loc[df["Churn_Flag"] == 0, "MonthlyCharges"].mean()

    kpis = pd.DataFrame([
        ["Total customers", total_customers],
        ["Churned customers", churned],
        ["Retained customers", retained],
        ["Overall churn rate (%)", round(churn_rate, 2)],
        ["Average tenure - churned (months)", round(avg_tenure_churned, 2)],
        ["Average tenure - retained (months)", round(avg_tenure_retained, 2)],
        ["Average monthly charges - churned (USD)", round(monthly_charges_churned, 2)],
        ["Average monthly charges - retained (USD)", round(monthly_charges_retained, 2)],
    ], columns=["KPI", "Value"])
    kpis.to_csv(OUT / "kpi_summary.csv", index=False)

    contract = save_segment(df, "Contract", "churn_by_contract.csv")
    tenure = save_segment(df, "Tenure_Group", "churn_by_tenure_group.csv")
    internet = save_segment(df, "InternetService", "churn_by_internet_service.csv")
    payment = save_segment(df, "PaymentMethod", "churn_by_payment_method.csv")

    # A concise overview chart, generated from actual data.
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    groups = [
        (contract, "Contract", "Churn rate by contract"),
        (tenure, "Tenure_Group", "Churn rate by tenure group"),
        (internet, "InternetService", "Churn rate by internet service"),
        (payment, "PaymentMethod", "Churn rate by payment method"),
    ]
    for ax, (table, col, title) in zip(axes.flat, groups):
        table = table.sort_values("churn_rate", ascending=False)
        ax.bar(table[col].astype(str), table["churn_rate"])
        ax.set_title(title)
        ax.set_ylabel("Observed churn rate (%)")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "churn_overview.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    # Export analysis tables to an Excel workbook.
    with pd.ExcelWriter(OUT / "churn_analysis.xlsx", engine="openpyxl") as writer:
        kpis.to_excel(writer, sheet_name="KPI Summary", index=False)
        contract.to_excel(writer, sheet_name="By Contract", index=False)
        tenure.to_excel(writer, sheet_name="By Tenure", index=False)
        internet.to_excel(writer, sheet_name="By Internet", index=False)
        payment.to_excel(writer, sheet_name="By Payment", index=False)

    # Load the cleaned table into SQLite for SQL practice.
    db_path = OUT / "customer_churn.sqlite"
    with sqlite3.connect(db_path) as conn:
        df.to_sql("customers", conn, if_exists="replace", index=False)

    log = [
        f"Raw rows: {original_rows}",
        f"Duplicate customer IDs: {duplicate_ids}",
        f"Blank TotalCharges before conversion: {blank_total_before}",
        f"Missing TotalCharges after numeric conversion: {missing_total}",
        f"Missing TotalCharges among zero-tenure customers: {zero_tenure_missing}",
        "Treatment: retained rows and filled blank TotalCharges with 0 for zero-tenure customers.",
        "Churn_Flag: Yes=1, No=0.",
        "No rows were removed by this script.",
    ]
    (OUT / "cleaning_log.txt").write_text("\n".join(log), encoding="utf-8")

    print("\n=== CUSTOMER CHURN ANALYSIS COMPLETE ===")
    print(kpis.to_string(index=False))
    print("\nCleaning notes:")
    print("\n".join(log))
    print(f"\nFiles saved in: {OUT.resolve()}")

if __name__ == "__main__":
    main()
