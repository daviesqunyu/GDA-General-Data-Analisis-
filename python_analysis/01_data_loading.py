"""
01_data_loading.py
Load data from SQLite into pandas DataFrames.
Nairobi Business Analytics — Davis Kunyu Wamalwa
"""

import sqlite3
import pandas as pd
from pathlib import Path


def get_db_path():
    """Resolve path to nairobi_business.db (run from project root or script dir)."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    db_path = project_root / "database" / "nairobi_business.db"
    if not db_path.exists():
        db_path = script_dir.parent / "database" / "nairobi_business.db"
    return db_path


def load_all_tables():
    """Connect to SQLite and load all 6 tables into pandas DataFrames."""
    db_path = get_db_path()
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at {db_path}. Run database/seed_data.py first.")
    conn = sqlite3.connect(str(db_path))

    tables = ["customers", "products", "orders", "order_items", "payments", "customer_support"]
    data = {}
    for table in tables:
        data[table] = pd.read_sql_query(f"SELECT * FROM {table}", conn)

    conn.close()
    return data


def main():
    data = load_all_tables()
    for name, df in data.items():
        print(f"\n=== {name} ===")
        print(f"Shape: {df.shape}")
        print(f"Dtypes:\n{df.dtypes}")
        print(f"Nulls:\n{df.isnull().sum()}")
        print(f"Head:\n{df.head()}")
        print(f"Summary:\n{df.describe(include='all')}")
    return data


if __name__ == "__main__":
    main()
