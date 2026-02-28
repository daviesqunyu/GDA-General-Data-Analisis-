"""
Tests for database schema and data integrity.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import unittest
import sqlite3
from pathlib import Path


def get_db_path():
    base = Path(__file__).resolve().parent.parent
    return base / "database" / "nairobi_business.db"


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = get_db_path()
        if not cls.db_path.exists():
            raise FileNotFoundError("Run database/seed_data.py first to create nairobi_business.db")
        cls.conn = sqlite3.connect(str(cls.db_path))

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_all_tables_exist(self):
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = {row[0] for row in cursor.fetchall()}
        expected = {"customers", "products", "orders", "order_items", "payments", "customer_support"}
        self.assertEqual(tables, expected, "All 6 tables must exist")

    def test_customers_minimum_rows(self):
        n = self.conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        self.assertGreaterEqual(n, 400, "Customers table should have at least 400 rows")

    def test_products_minimum_rows(self):
        n = self.conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        self.assertGreaterEqual(n, 40, "Products table should have at least 40 rows")

    def test_orders_minimum_rows(self):
        n = self.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        self.assertGreaterEqual(n, 1500, "Orders table should have at least 1500 rows")

    def test_order_items_minimum_rows(self):
        n = self.conn.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
        self.assertGreaterEqual(n, 3000, "Order_items table should have at least 3000 rows")

    def test_payments_minimum_rows(self):
        n = self.conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0]
        self.assertGreaterEqual(n, 1500, "Payments table should have at least 1500 rows")

    def test_support_minimum_rows(self):
        n = self.conn.execute("SELECT COUNT(*) FROM customer_support").fetchone()[0]
        self.assertGreaterEqual(n, 200, "Customer_support table should have at least 200 rows")

    def test_no_null_customer_email(self):
        n = self.conn.execute("SELECT COUNT(*) FROM customers WHERE email IS NULL OR email = ''").fetchone()[0]
        self.assertEqual(n, 0, "Customer email must not be null/empty")

    def test_no_null_order_total(self):
        n = self.conn.execute("SELECT COUNT(*) FROM orders WHERE total_amount IS NULL").fetchone()[0]
        self.assertEqual(n, 0, "Order total_amount must not be null")

    def test_no_null_product_price(self):
        n = self.conn.execute("SELECT COUNT(*) FROM products WHERE unit_price IS NULL").fetchone()[0]
        self.assertEqual(n, 0, "Product unit_price must not be null")

    def test_foreign_key_orders_customers(self):
        cursor = self.conn.execute("""
            SELECT COUNT(*) FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
        """)
        n = cursor.fetchone()[0]
        self.assertEqual(n, 0, "Every order must reference a valid customer_id")

    def test_date_format_orders(self):
        cursor = self.conn.execute("""
            SELECT order_date FROM orders WHERE order_date IS NOT NULL LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            self.assertRegex(row[0], r"^\d{4}-\d{2}-\d{2}$", "order_date should be YYYY-MM-DD")


if __name__ == "__main__":
    unittest.main()
