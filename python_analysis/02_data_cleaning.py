"""
02_data_cleaning.py
Data cleaning: nulls, duplicates, outliers, type casting.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import pandas as pd
import sqlite3
from pathlib import Path


def get_db_path():
    base = Path(__file__).resolve().parent.parent
    return base / "database" / "nairobi_business.db"


def load_all():
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    tables = ["customers", "products", "orders", "order_items", "payments", "customer_support"]
    return {t: pd.read_sql_query(f"SELECT * FROM {t}", conn) for t in tables}


def check_nulls(df):
    """Report missing values per column with percentage."""
    null_counts = df.isnull().sum()
    null_pct = (df.isnull().sum() / len(df) * 100).round(2)
    report = pd.DataFrame({"null_count": null_counts, "null_pct": null_pct})
    return report[report["null_count"] > 0]


def check_duplicates(df):
    """Find and report duplicate rows."""
    n_dup = df.duplicated().sum()
    return n_dup, df[df.duplicated(keep=False)]


def fix_data_types(df, table_name):
    """Convert date strings to datetime, numeric strings to float."""
    df = df.copy()
    date_cols = {
        "customers": ["registration_date"],
        "products": ["created_at"],
        "orders": ["order_date", "delivery_date"],
        "payments": ["payment_date"],
        "customer_support": ["created_date", "resolved_date"],
    }
    for col in date_cols.get(table_name, []):
        if col in df.columns and df[col].dtype == object:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    numeric_cols = [c for c in df.columns if df[c].dtype == object and df[c].replace("", None).notna().any()]
    for col in ["unit_price", "cost_price", "total_amount", "subtotal", "amount_paid", "discount_applied"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def handle_outliers(df, column):
    """Detect outliers using IQR method, report them."""
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return pd.DataFrame()
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower) | (df[column] > upper)]
    return outliers


def clean_all_tables():
    """Run all cleaning on all 6 tables, return cleaned DataFrames."""
    data = load_all()
    report_lines = ["# Data Quality Report\n"]

    for name, df in data.items():
        df = fix_data_types(df, name)
        null_report = check_nulls(df)
        n_dup, dup_df = check_duplicates(df)
        report_lines.append(f"## {name}\n")
        report_lines.append(f"- Rows: {len(df)}\n")
        if len(null_report) > 0:
            report_lines.append("Nulls:\n" + null_report.to_string() + "\n\n")
        report_lines.append(f"Duplicate rows: {n_dup}\n\n")
        if name == "orders" and "total_amount" in df.columns:
            out = handle_outliers(df, "total_amount")
            report_lines.append(f"Outliers (total_amount, IQR): {len(out)}\n\n")
        data[name] = df

    reports_dir = Path(__file__).resolve().parent.parent / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "data_quality_report.md").write_text("\n".join(report_lines), encoding="utf-8")
    print("Saved reports/data_quality_report.md")
    return data


def main():
    clean_all_tables()
    print("Data cleaning complete.")


if __name__ == "__main__":
    main()
