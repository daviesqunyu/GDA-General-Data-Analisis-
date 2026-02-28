"""
Tests for SQL query results.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import unittest
import sqlite3
from pathlib import Path


def get_db_path():
    base = Path(__file__).resolve().parent.parent
    return base / "database" / "nairobi_business.db"


class TestQueries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = get_db_path()
        if not cls.db_path.exists():
            raise FileNotFoundError("Run database/seed_data.py first")
        cls.conn = sqlite3.connect(str(cls.db_path))

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_monthly_revenue_twelve_months(self):
        rows = self.conn.execute("""
            SELECT strftime('%Y-%m', order_date) AS month
            FROM orders
            WHERE status NOT IN ('Cancelled', 'Returned')
              AND order_date >= '2024-01-01' AND order_date <= '2024-12-31'
            GROUP BY strftime('%Y-%m', order_date)
            ORDER BY month
        """).fetchall()
        self.assertEqual(len(rows), 12, "Monthly revenue query should return 12 rows (one per month)")

    def test_top_customers_row_count(self):
        rows = self.conn.execute("""
            SELECT c.customer_id, SUM(o.total_amount) AS total
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.status NOT IN ('Cancelled', 'Returned')
            GROUP BY c.customer_id
            ORDER BY total DESC
            LIMIT 20
        """).fetchall()
        self.assertLessEqual(len(rows), 20, "Top customers should return at most 20 rows")
        self.assertGreater(len(rows), 0, "Top customers should return at least 1 row")

    def test_rfm_scores_range(self):
        """RFM raw query returns recency, frequency, monetary; we check values are in reasonable range."""
        rows = self.conn.execute("""
            SELECT 
                JULIANDAY('2024-12-31') - JULIANDAY(MAX(o.order_date)) AS recency_days,
                COUNT(o.order_id) AS frequency,
                SUM(o.total_amount) AS monetary
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.status NOT IN ('Cancelled', 'Returned')
            GROUP BY c.customer_id
            LIMIT 10
        """).fetchall()
        for recency, freq, monetary in rows:
            self.assertGreaterEqual(recency, 0, "Recency should be non-negative")
            self.assertGreaterEqual(freq, 1, "Frequency should be at least 1")
            self.assertGreater(monetary, 0, "Monetary should be positive")

    def test_window_function_no_null_rank(self):
        rows = self.conn.execute("""
            SELECT customer_id, total_spent,
                   RANK() OVER (ORDER BY total_spent DESC) AS rk
            FROM (
                SELECT c.customer_id, ROUND(SUM(o.total_amount),2) AS total_spent
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                WHERE o.status NOT IN ('Cancelled', 'Returned')
                GROUP BY c.customer_id
            )
            LIMIT 100
        """).fetchall()
        for row in rows:
            self.assertIsNotNone(row[2], "Rank should not be null")
            self.assertGreater(row[2], 0, "Rank should be positive")


if __name__ == "__main__":
    unittest.main()
