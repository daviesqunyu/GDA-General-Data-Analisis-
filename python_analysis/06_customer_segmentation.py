"""
06_customer_segmentation.py
RFM scores + K-Means clustering; segment labels; save scatter and bar charts.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def get_db_path():
    base = Path(__file__).resolve().parent.parent
    return base / "database" / "nairobi_business.db"


def charts_dir():
    d = Path(__file__).resolve().parent.parent / "reports" / "charts"
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_rfm(conn):
    return pd.read_sql_query("""
        SELECT c.customer_id,
               JULIANDAY('2024-12-31') - JULIANDAY(MAX(o.order_date)) AS recency_days,
               COUNT(o.order_id) AS frequency,
               SUM(o.total_amount) AS monetary
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status NOT IN ('Cancelled', 'Returned')
        GROUP BY c.customer_id
    """, conn)


def rfm_quintile_scores(df):
    """Score 1-5 for R (5=most recent), F (5=most), M (5=highest)."""
    df = df.copy()
    df["R_score"] = pd.qcut(df["recency_days"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    df["F_score"] = pd.qcut(df["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    df["M_score"] = pd.qcut(df["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    return df


def main():
    db_path = get_db_path()
    if not db_path.exists():
        print("Database not found. Run database/seed_data.py first.")
        return
    conn = sqlite3.connect(str(db_path))
    rfm = load_rfm(conn)
    conn.close()

    rfm = rfm_quintile_scores(rfm)
    X = rfm[["recency_days", "frequency", "monetary"]].copy()
    X_scaled = StandardScaler().fit_transform(X)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    rfm["segment_id"] = kmeans.fit_predict(X_scaled)

    # Label segments by mean RFM (Champions: high F&M low R; Loyal; At Risk; Lost)
    seg_means = rfm.groupby("segment_id")[["recency_days", "frequency", "monetary"]].mean()
    seg_means["recency_rank"] = seg_means["recency_days"].rank()
    seg_means["monetary_rank"] = seg_means["monetary"].rank(ascending=False)
    segment_names = {}
    for sid in seg_means.index:
        r_low = seg_means.loc[sid, "recency_days"] < rfm["recency_days"].median()
        m_high = seg_means.loc[sid, "monetary"] > rfm["monetary"].median()
        if m_high and r_low:
            segment_names[sid] = "Champions"
        elif m_high and not r_low:
            segment_names[sid] = "Loyal Customers"
        elif not r_low:
            segment_names[sid] = "At Risk"
        else:
            segment_names[sid] = "Lost"
    rfm["segment"] = rfm["segment_id"].map(segment_names)

    print("--- Segment sizes ---")
    print(rfm["segment"].value_counts())
    print("\n--- Avg RFM by segment ---")
    print(rfm.groupby("segment")[["recency_days", "frequency", "monetary"]].mean().round(2))

    # Scatter: frequency vs monetary, coloured by segment
    plt.figure(figsize=(10, 6))
    for seg in rfm["segment"].unique():
        sub = rfm[rfm["segment"] == seg]
        plt.scatter(sub["frequency"], sub["monetary"], label=seg, alpha=0.6)
    plt.xlabel("Frequency")
    plt.ylabel("Monetary (KSh)")
    plt.title("RFM Customer Segments (K-Means k=4)")
    plt.legend()
    plt.savefig(charts_dir() / "rfm_segments_scatter.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved rfm_segments_scatter.png")

    # Bar: customers per segment
    plt.figure(figsize=(8, 5))
    counts = rfm["segment"].value_counts()
    plt.bar(counts.index, counts.values, color=["#2ecc71", "#3498db", "#e74c3c", "#95a5a6"])
    plt.title("Customer Count by Segment")
    plt.ylabel("Count")
    plt.savefig(charts_dir() / "segment_distribution_bar.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved segment_distribution_bar.png")
    print("\nCustomer segmentation complete.")


if __name__ == "__main__":
    main()
