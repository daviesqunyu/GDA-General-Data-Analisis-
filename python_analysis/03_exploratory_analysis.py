"""
03_exploratory_analysis.py
EDA: distributions, correlations, descriptive stats.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import sqlite3
import pandas as pd
from pathlib import Path


def get_db_path():
    base = Path(__file__).resolve().parent.parent
    return base / "database" / "nairobi_business.db"


def load_conn():
    return sqlite3.connect(str(get_db_path()))


def describe_sales():
    """Descriptive statistics on order amounts."""
    conn = load_conn()
    df = pd.read_sql_query(
        "SELECT total_amount FROM orders WHERE status NOT IN ('Cancelled', 'Returned')",
        conn,
    )
    conn.close()
    print("--- Sales (order total_amount) ---")
    print(df["total_amount"].describe())
    return df


def revenue_by_month():
    """Monthly revenue summary table."""
    conn = load_conn()
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue
        FROM orders
        WHERE status NOT IN ('Cancelled', 'Returned') AND order_date >= '2024-01-01'
        GROUP BY strftime('%Y-%m', order_date)
        ORDER BY month
    """, conn)
    conn.close()
    print("\n--- Revenue by month ---")
    print(df.to_string())
    return df


def top_customers(n=10):
    """Top N customers by spend."""
    conn = load_conn()
    df = pd.read_sql_query("""
        SELECT c.customer_id, c.first_name, c.last_name, SUM(o.total_amount) AS total_spend
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status NOT IN ('Cancelled', 'Returned')
        GROUP BY c.customer_id ORDER BY total_spend DESC LIMIT ?
    """, conn, params=(n,))
    conn.close()
    print(f"\n--- Top {n} customers by spend ---")
    print(df.to_string())
    return df


def top_products(n=10):
    """Top N products by revenue."""
    conn = load_conn()
    df = pd.read_sql_query("""
        SELECT p.product_name, p.category, SUM(oi.subtotal) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status NOT IN ('Cancelled', 'Returned')
        GROUP BY p.product_id ORDER BY revenue DESC LIMIT ?
    """, conn, params=(n,))
    conn.close()
    print(f"\n--- Top {n} products by revenue ---")
    print(df.to_string())
    return df


def correlation_analysis():
    """Correlation matrix between numeric variables."""
    conn = load_conn()
    df = pd.read_sql_query("""
        SELECT o.total_amount, o.discount_applied, oi.quantity, oi.unit_price, oi.subtotal
        FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status NOT IN ('Cancelled', 'Returned')
        LIMIT 5000
    """, conn)
    conn.close()
    numeric = df.select_dtypes(include=["number"])
    corr = numeric.corr()
    print("\n--- Correlation matrix ---")
    print(corr.to_string())
    return corr


def customer_distribution():
    """Customers per location."""
    conn = load_conn()
    df = pd.read_sql_query("""
        SELECT location, COUNT(*) AS count FROM customers GROUP BY location ORDER BY count DESC
    """, conn)
    conn.close()
    print("\n--- Customer distribution by location ---")
    print(df.to_string())
    return df


def main():
    describe_sales()
    revenue_by_month()
    top_customers(10)
    top_products(10)
    correlation_analysis()
    customer_distribution()
    print("\nEDA complete.")


if __name__ == "__main__":
    main()
