"""
04_visualisations.py
Charts: bar, line, scatter, heatmap, box plots — saved to reports/charts/
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np


def get_db_path():
    base = Path(__file__).resolve().parent.parent
    return base / "database" / "nairobi_business.db"


def charts_dir():
    d = Path(__file__).resolve().parent.parent / "reports" / "charts"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save(name, dpi=150):
    out = charts_dir() / name
    plt.savefig(out, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Saved {name}")


def monthly_revenue_bar(conn):
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue
        FROM orders WHERE status NOT IN ('Cancelled', 'Returned') AND order_date >= '2024-01-01'
        GROUP BY strftime('%Y-%m', order_date) ORDER BY month
    """, conn)
    plt.figure(figsize=(10, 5))
    plt.bar(df["month"], df["revenue"], color="steelblue", edgecolor="black")
    plt.title("Monthly Revenue (KSh) — 2024")
    plt.xlabel("Month")
    plt.ylabel("Revenue (KSh)")
    plt.xticks(rotation=45)
    save("monthly_revenue_bar.png")


def revenue_trend_line(conn):
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue
        FROM orders WHERE status NOT IN ('Cancelled', 'Returned') AND order_date >= '2024-01-01'
        GROUP BY strftime('%Y-%m', order_date) ORDER BY month
    """, conn)
    x = np.arange(len(df))
    z = np.polyfit(x, df["revenue"], 1)
    p = np.poly1d(z)
    plt.figure(figsize=(10, 5))
    plt.plot(df["month"], df["revenue"], marker="o", label="Revenue")
    plt.plot(df["month"], p(x), "r--", label="Trend")
    plt.title("Revenue Trend — 2024")
    plt.xlabel("Month")
    plt.ylabel("Revenue (KSh)")
    plt.legend()
    plt.xticks(rotation=45)
    save("revenue_trend_line.png")


def category_pie(conn):
    df = pd.read_sql_query("""
        SELECT p.category, SUM(oi.subtotal) AS revenue
        FROM order_items oi JOIN products p ON oi.product_id = p.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status NOT IN ('Cancelled', 'Returned')
        GROUP BY p.category
    """, conn)
    plt.figure(figsize=(8, 8))
    plt.pie(df["revenue"], labels=df["category"], autopct="%1.1f%%", startangle=90)
    plt.title("Revenue by Product Category")
    save("category_pie.png")


def payment_method_bar(conn):
    df = pd.read_sql_query("""
        SELECT payment_method, COUNT(*) AS cnt FROM orders
        WHERE status NOT IN ('Cancelled', 'Returned') GROUP BY payment_method
    """, conn)
    plt.figure(figsize=(8, 5))
    plt.barh(df["payment_method"], df["cnt"], color="teal")
    plt.title("Orders by Payment Method")
    plt.xlabel("Number of Orders")
    save("payment_method_bar.png")


def customer_location_bar(conn):
    df = pd.read_sql_query("""
        SELECT location, COUNT(*) AS cnt FROM customers GROUP BY location ORDER BY cnt DESC
    """, conn)
    plt.figure(figsize=(10, 6))
    plt.bar(df["location"], df["cnt"], color="coral", edgecolor="black")
    plt.title("Customers by Nairobi Neighbourhood")
    plt.xlabel("Location")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    save("customer_location_bar.png")


def order_value_histogram(conn):
    df = pd.read_sql_query("""
        SELECT total_amount FROM orders WHERE status NOT IN ('Cancelled', 'Returned')
    """, conn)
    plt.figure(figsize=(8, 5))
    plt.hist(df["total_amount"], bins=50, density=True, alpha=0.7, color="green", edgecolor="black")
    mu, std = df["total_amount"].mean(), df["total_amount"].std()
    x = np.linspace(df["total_amount"].min(), df["total_amount"].max(), 100)
    plt.plot(x, (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / std) ** 2), "r-", label="Normal")
    plt.title("Distribution of Order Values (KSh)")
    plt.xlabel("Order Value")
    plt.ylabel("Density")
    plt.legend()
    save("order_value_histogram.png")


def correlation_heatmap(conn):
    df = pd.read_sql_query("""
        SELECT o.total_amount, o.discount_applied, oi.quantity, oi.unit_price, oi.subtotal
        FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status NOT IN ('Cancelled', 'Returned') LIMIT 3000
    """, conn)
    plt.figure(figsize=(8, 6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", center=0, fmt=".2f")
    plt.title("Correlation Heatmap (Numeric Variables)")
    save("correlation_heatmap.png")


def top10_products_bar(conn):
    df = pd.read_sql_query("""
        SELECT p.product_name, SUM(oi.subtotal) AS revenue
        FROM order_items oi JOIN products p ON oi.product_id = p.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status NOT IN ('Cancelled', 'Returned')
        GROUP BY p.product_id ORDER BY revenue DESC LIMIT 10
    """, conn)
    plt.figure(figsize=(10, 6))
    plt.barh(df["product_name"].str[:30], df["revenue"], color="purple", alpha=0.8)
    plt.title("Top 10 Products by Revenue (KSh)")
    plt.xlabel("Revenue")
    save("top10_products_bar.png")


def monthly_orders_vs_revenue(conn):
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', order_date) AS month,
               COUNT(*) AS orders,
               SUM(total_amount) AS revenue
        FROM orders WHERE status NOT IN ('Cancelled', 'Returned') AND order_date >= '2024-01-01'
        GROUP BY strftime('%Y-%m', order_date) ORDER BY month
    """, conn)
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df["month"], df["orders"], "b-o", label="Orders")
    ax1.set_ylabel("Order count", color="b")
    ax2 = ax1.twinx()
    ax2.plot(df["month"], df["revenue"], "g-s", label="Revenue")
    ax2.set_ylabel("Revenue (KSh)", color="g")
    plt.title("Monthly Orders vs Revenue — 2024")
    plt.xlabel("Month")
    plt.xticks(rotation=45)
    save("monthly_orders_vs_revenue.png")


def satisfaction_boxplot(conn):
    df = pd.read_sql_query("""
        SELECT issue_type, satisfaction_score FROM customer_support WHERE satisfaction_score IS NOT NULL
    """, conn)
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x="issue_type", y="satisfaction_score")
    plt.title("Satisfaction Score by Issue Type")
    plt.xlabel("Issue Type")
    plt.ylabel("Satisfaction (1-5)")
    plt.xticks(rotation=45)
    save("satisfaction_boxplot.png")


def main():
    db_path = get_db_path()
    if not db_path.exists():
        print("Database not found. Run database/seed_data.py first.")
        return
    conn = sqlite3.connect(str(db_path))
    monthly_revenue_bar(conn)
    revenue_trend_line(conn)
    category_pie(conn)
    payment_method_bar(conn)
    customer_location_bar(conn)
    order_value_histogram(conn)
    correlation_heatmap(conn)
    top10_products_bar(conn)
    monthly_orders_vs_revenue(conn)
    satisfaction_boxplot(conn)
    conn.close()
    print("All 10 charts saved to reports/charts/")


if __name__ == "__main__":
    main()
