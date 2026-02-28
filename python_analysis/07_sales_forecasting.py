"""
07_sales_forecasting.py
Linear regression on monthly revenue; train Jan-Sep, test Oct-Dec; forecast Jan-Mar 2025.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def get_db_path():
    base = Path(__file__).resolve().parent.parent
    return base / "database" / "nairobi_business.db"


def charts_dir():
    d = Path(__file__).resolve().parent.parent / "reports" / "charts"
    d.mkdir(parents=True, exist_ok=True)
    return d


def main():
    db_path = get_db_path()
    if not db_path.exists():
        print("Database not found. Run database/seed_data.py first.")
        return
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue
        FROM orders
        WHERE status NOT IN ('Cancelled', 'Returned') AND order_date >= '2024-01-01'
        GROUP BY strftime('%Y-%m', order_date)
        ORDER BY month
    """, conn)
    conn.close()

    df["month_idx"] = np.arange(len(df))
    train = df[df["month_idx"] < 9]   # Jan-Sep
    test = df[df["month_idx"] >= 9]   # Oct-Dec

    X_train = train[["month_idx"]]
    y_train = train["revenue"]
    X_test = test[["month_idx"]]
    y_test = test["revenue"]

    model = LinearRegression().fit(X_train, y_train)
    pred_test = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred_test)
    rmse = np.sqrt(np.mean((y_test - pred_test) ** 2))

    # Forecast Jan-Mar 2025 (indices 12, 13, 14)
    future_idx = pd.DataFrame({"month_idx": [12, 13, 14]})
    forecast = model.predict(future_idx)
    jan_2025 = forecast[0]

    print("--- Sales forecasting (Linear Regression) ---")
    print(f"Test MAE: {mae:.2f} KSh")
    print(f"Test RMSE: {rmse:.2f} KSh")
    print(f"Based on 2024 data, forecast January 2025 revenue: KSh {jan_2025:,.2f}")

    # Chart: actual, predicted, forecast
    plt.figure(figsize=(10, 5))
    months = df["month"].tolist()
    plt.plot(months, df["revenue"], "b-o", label="Actual 2024")
    pred_all = model.predict(df[["month_idx"]])
    plt.plot(months, pred_all, "g--", label="Fitted")
    future_months = ["2025-01", "2025-02", "2025-03"]
    plt.plot(future_months, forecast, "r-s", label="Forecast 2025")
    plt.xlabel("Month")
    plt.ylabel("Revenue (KSh)")
    plt.title("Sales Forecast — Actual vs Predicted vs Forecast")
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig(charts_dir() / "sales_forecast_chart.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved sales_forecast_chart.png")
    print("\nSales forecasting complete.")


if __name__ == "__main__":
    main()
