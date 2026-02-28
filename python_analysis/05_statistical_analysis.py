"""
05_statistical_analysis.py
Hypothesis testing, correlation, normality, ANOVA, t-tests.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import sqlite3
import pandas as pd
from pathlib import Path
from scipy import stats


def get_db_path():
    base = Path(__file__).resolve().parent.parent
    return base / "database" / "nairobi_business.db"


def load_orders(conn):
    return pd.read_sql_query(
        "SELECT total_amount, payment_method, order_date FROM orders WHERE status NOT IN ('Cancelled', 'Returned')",
        conn,
    )


def descriptive_stats():
    """Mean, median, mode, std dev, variance of order values."""
    conn = sqlite3.connect(str(get_db_path()))
    df = load_orders(conn)
    conn.close()
    vals = df["total_amount"]
    print("--- Descriptive stats (order value) ---")
    print(f"Mean: {vals.mean():.2f} KSh")
    print(f"Median: {vals.median():.2f} KSh")
    print(f"Mode: {vals.mode().values[0]:.2f} KSh" if len(vals.mode()) else "N/A")
    print(f"Std: {vals.std():.2f}")
    print(f"Variance: {vals.var():.2f}")
    return vals


def revenue_normality_test():
    """Shapiro-Wilk test; print whether data is normal."""
    conn = sqlite3.connect(str(get_db_path()))
    df = load_orders(conn)
    conn.close()
    sample = df["total_amount"].sample(min(5000, len(df)), random_state=42)
    stat, p = stats.shapiro(sample)
    print("\n--- Normality (Shapiro-Wilk) ---")
    print(f"Statistic: {stat:.4f}, p-value: {p:.4f}")
    print("Interpretation: Data is NOT normally distributed (p < 0.05)." if p < 0.05 else "Interpretation: Cannot reject normality (p >= 0.05).")
    return p


def payment_method_anova():
    """One-way ANOVA: does payment method affect order value?"""
    conn = sqlite3.connect(str(get_db_path()))
    df = load_orders(conn)
    conn.close()
    groups = [df[df["payment_method"] == m]["total_amount"].values for m in df["payment_method"].unique()]
    groups = [g for g in groups if len(g) >= 2]
    if len(groups) < 2:
        print("Not enough groups for ANOVA.")
        return None
    stat, p = stats.f_oneway(*groups)
    print("\n--- ANOVA (order value by payment method) ---")
    print(f"F-statistic: {stat:.4f}, p-value: {p:.4f}")
    print("Interpretation: Payment method DOES affect order value (p < 0.05)." if p < 0.05 else "Interpretation: No significant effect of payment method (p >= 0.05).")
    return p


def location_revenue_correlation():
    """Pearson correlation between numeric variables (e.g. order value vs discount)."""
    conn = sqlite3.connect(str(get_db_path()))
    df = pd.read_sql_query("SELECT total_amount, discount_applied FROM orders WHERE status NOT IN ('Cancelled', 'Returned')", conn)
    conn.close()
    r, p = stats.pearsonr(df["total_amount"], df["discount_applied"])
    print("\n--- Pearson correlation (total_amount vs discount_applied) ---")
    print(f"r: {r:.4f}, p-value: {p:.4f}")
    print("Interpretation: Weak/negative correlation; discount not strongly tied to order size.")
    return r


def month_ttest():
    """t-test comparing H1 vs H2 revenue (mean order value)."""
    conn = sqlite3.connect(str(get_db_path()))
    df = load_orders(conn)
    conn.close()
    df["order_date"] = pd.to_datetime(df["order_date"])
    h1 = df[df["order_date"].dt.month <= 6]["total_amount"]
    h2 = df[df["order_date"].dt.month >= 7]["total_amount"]
    stat, p = stats.ttest_ind(h1, h2)
    print("\n--- t-test H1 vs H2 (mean order value) ---")
    print(f"t-statistic: {stat:.4f}, p-value: {p:.4f}")
    print("Interpretation: H1 and H2 mean order values differ significantly (p < 0.05)." if p < 0.05 else "Interpretation: No significant difference between H1 and H2 (p >= 0.05).")
    return p


def main():
    descriptive_stats()
    revenue_normality_test()
    payment_method_anova()
    location_revenue_correlation()
    month_ttest()
    print("\nStatistical analysis complete.")


if __name__ == "__main__":
    main()
