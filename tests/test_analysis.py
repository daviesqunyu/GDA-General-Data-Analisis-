"""
Tests for Python analysis functions and outputs.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import unittest
import pandas as pd
import sys
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _load_cleaning_module():
    spec = importlib.util.spec_from_file_location(
        "data_cleaning",
        ROOT / "python_analysis" / "02_data_cleaning.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestAnalysis(unittest.TestCase):
    def test_check_nulls_returns_dataframe(self):
        mod = _load_cleaning_module()
        df = pd.DataFrame({"a": [1, 2, None], "b": [1, 1, 1]})
        result = mod.check_nulls(df)
        self.assertIsInstance(result, pd.DataFrame, "check_nulls should return a DataFrame")

    def test_handle_outliers_identifies_outlier(self):
        mod = _load_cleaning_module()
        df = pd.DataFrame({"x": [10, 12, 11, 13, 100]})
        result = mod.handle_outliers(df, "x")
        self.assertGreaterEqual(len(result), 1, "handle_outliers should identify at least 1 outlier in test data")

    def test_chart_files_created(self):
        charts_dir = ROOT / "reports" / "charts"
        if not charts_dir.exists():
            self.skipTest("Charts not generated yet; run python_analysis/04_visualisations.py first")
        expected = [
            "monthly_revenue_bar.png",
            "revenue_trend_line.png",
            "category_pie.png",
            "payment_method_bar.png",
            "customer_location_bar.png",
            "order_value_histogram.png",
            "correlation_heatmap.png",
            "top10_products_bar.png",
            "monthly_orders_vs_revenue.png",
            "satisfaction_boxplot.png",
        ]
        for name in expected:
            path = charts_dir / name
            self.assertTrue(path.exists(), f"Chart {name} should exist after running visualisations script")

    def test_forecast_positive(self):
        """Sales forecast for Jan 2025 should return a positive number when run."""
        db_path = ROOT / "database" / "nairobi_business.db"
        if not db_path.exists():
            self.skipTest("Database not found; run seed_data.py first")
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        df = pd.read_sql_query("""
            SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue
            FROM orders
            WHERE status NOT IN ('Cancelled', 'Returned') AND order_date >= '2024-01-01'
            GROUP BY strftime('%Y-%m', order_date) ORDER BY month
        """, conn)
        conn.close()
        if len(df) < 2:
            self.skipTest("Not enough monthly data")
        from sklearn.linear_model import LinearRegression
        import numpy as np
        X = np.arange(len(df)).reshape(-1, 1)
        y = df["revenue"].values
        model = LinearRegression().fit(X, y)
        jan2025 = model.predict([[12]])[0]
        self.assertGreater(jan2025, 0, "Forecast January 2025 revenue should be positive")


if __name__ == "__main__":
    unittest.main()
