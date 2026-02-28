"""
Nairobi Business Intelligence & Sales Analytics System
Seed script: generates realistic data and populates SQLite database.
Author: Davis Kunyu Wamalwa
"""

import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

# Optional: use faker for names/emails; fallback to simple lists if not installed
try:
    from faker import Faker
    fake = Faker()
    USE_FAKER = True
except ImportError:
    USE_FAKER = False

# Nairobi neighbourhoods
LOCATIONS = [
    "Westlands", "Karen", "CBD", "Kasarani", "Kilimani", "Lavington",
    "South B", "South C", "Eastleigh", "Parklands", "Ngong Road", "Langata",
    "Ruaka", "Githurai", "Rongai"
]

# Customer types
CUSTOMER_TYPES = ["Individual", "SME", "Corporate"]
# Weights: more individuals, fewer corporate
CUSTOMER_TYPE_WEIGHTS = [0.65, 0.25, 0.10]

# Product categories and sample products (realistic Kenyan context)
CATEGORIES = ["Electronics", "Clothing", "Food", "Home", "Beauty", "Sports"]

PRODUCTS_BY_CATEGORY = {
    "Electronics": [
        "Samsung Galaxy A14", "Infinix Hot 30", "Tecno Spark 10", "Smart TV 32\"",
        "Bluetooth Speaker", "Power Bank 20000mAh", "USB Cable Pack", "Earbuds",
        "Tablet 10\"", "LED Bulb Pack"
    ],
    "Clothing": [
        "Men's Shirt", "Women's Dress", "Jeans", "Kitenge Shirt", "School Uniform",
        "Sports Jersey", "Winter Jacket", "Sandals", "Canvas Shoes", "Belt"
    ],
    "Food": [
        "Rice 2kg", "Cooking Oil 1L", "Maize Flour 2kg", "Sugar 1kg", "Tea Leaves 500g",
        "Bread Loaf", "Milk 1L", "Eggs Tray", "Fresh Vegetables Pack", "Fruits Basket"
    ],
    "Home": [
        "Plastic Chair", "Storage Box", "Mosquito Net", "Water Dispenser",
        "Blanket", "Pillow Set", "Curtains", "Frying Pan", "Saucepan Set", "Broom"
    ],
    "Beauty": [
        "Body Lotion", "Shampoo 400ml", "Soap Bar Pack", "Hair Oil", "Face Cream",
        "Lip Balm", "Deodorant", "Toothpaste", "Sanitary Pads Pack", "Razor Pack"
    ],
    "Sports": [
        "Football", "Running Shoes", "Yoga Mat", "Dumbbells 5kg", "Jump Rope",
        "Sports Bottle", "Gym Bag", "Cycling Helmet", "Tennis Racket", "Swim Goggles"
    ]
}

SUPPLIERS = ["Local Wholesale", "Import Direct", "Nairobi Distributors", "East Africa Supplies", "TechHub KE"]

# Order statuses
ORDER_STATUSES = ["Pending", "Processing", "Delivered", "Cancelled", "Returned"]
ORDER_STATUS_WEIGHTS = [0.05, 0.05, 0.82, 0.05, 0.03]

# Payment methods — M-Pesa dominant in Kenya
PAYMENT_METHODS = ["M-Pesa", "Cash", "Card", "Bank Transfer"]
PAYMENT_WEIGHTS = [0.60, 0.20, 0.12, 0.08]

# Support
ISSUE_TYPES = ["Delivery", "Payment", "Product Quality", "Returns", "Other"]
SUPPORT_STATUSES = ["Open", "Resolved", "Escalated"]

# Kenyan first/last names for fallback when faker not used
FIRST_NAMES = [
    "James", "John", "Peter", "Mary", "Grace", "Faith", "Joseph", "David", "Daniel",
    "Elizabeth", "Anne", "Lucy", "Michael", "Stephen", "Paul", "Sarah", "Jane", "Ruth"
]
LAST_NAMES = [
    "Ochieng", "Otieno", "Omondi", "Odhiambo", "Owino", "Akinyi", "Adhiambo", "Achieng",
    "Kamau", "Kipchoge", "Wanjiku", "Wambui", "Njoroge", "Mutua", "Muthoni", "Kariuki"
]


def get_db_path():
    """Return path to SQLite database file."""
    base = Path(__file__).resolve().parent
    return base / "nairobi_business.db"


def run_schema(conn):
    """Execute schema.sql to create tables."""
    schema_path = Path(__file__).resolve().parent / "schema.sql"
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()


def generate_customers(n=500):
    """Generate n customers with Nairobi locations and Kenyan context."""
    rows = []
    seen_emails = set()
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 6, 30)

    for i in range(1, n + 1):
        if USE_FAKER:
            first = fake.first_name()
            last = fake.last_name()
            email = f"{first.lower()}.{last.lower()}{i}@example.com"
        else:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            email = f"{first.lower()}.{last.lower()}{i}@example.com"
        if email in seen_emails:
            email = f"user{i}_{random.randint(1000,9999)}@example.com"
        seen_emails.add(email)

        phone = f"07{random.randint(10,99)} {random.randint(100000,999999)}" if random.random() > 0.1 else None
        location = random.choice(LOCATIONS)
        customer_type = random.choices(CUSTOMER_TYPES, weights=CUSTOMER_TYPE_WEIGHTS)[0]
        reg = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        registration_date = reg.strftime("%Y-%m-%d")
        is_active = 1 if random.random() > 0.08 else 0  # ~8% churned

        rows.append((first, last, email, phone, location, customer_type, registration_date, is_active))
    return rows


def generate_products():
    """Generate 50 products across categories with KSh prices."""
    rows = []
    pid = 1
    for category in CATEGORIES:
        names = PRODUCTS_BY_CATEGORY.get(category, ["Generic Item"])
        for name in names:
            if pid > 50:
                break
            # Realistic KSh: electronics higher, food lower
            if category == "Electronics":
                unit_price = round(random.uniform(1500, 45000), 2)
            elif category == "Clothing":
                unit_price = round(random.uniform(500, 8000), 2)
            elif category == "Food":
                unit_price = round(random.uniform(80, 800), 2)
            elif category == "Home":
                unit_price = round(random.uniform(400, 12000), 2)
            elif category == "Beauty":
                unit_price = round(random.uniform(150, 2500), 2)
            else:
                unit_price = round(random.uniform(600, 15000), 2)
            cost_price = round(unit_price * random.uniform(0.5, 0.85), 2)
            stock = random.randint(0, 100)
            if random.random() < 0.15:
                stock = random.randint(0, 9)  # Some low stock
            supplier = random.choice(SUPPLIERS)
            created = (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 400))).strftime("%Y-%m-%d")
            rows.append((name, category, unit_price, cost_price, stock, supplier, created))
            pid += 1
    return rows[:50]


def generate_orders(customer_ids, n_orders=2000):
    """Generate orders from Jan 2024 to Dec 2024 with seasonal pattern."""
    rows = []
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    # Seasonal weights: higher in Nov-Dec, lower Jan-Feb
    month_weights = [
        0.06, 0.06, 0.07, 0.08, 0.08, 0.08, 0.08, 0.08, 0.09, 0.09, 0.11, 0.12
    ]
    for i in range(1, n_orders + 1):
        cust_id = random.choice(customer_ids)
        # Pick month by weight then random day
        m = random.choices(range(1, 13), weights=month_weights)[0]
        day = random.randint(1, 28)
        order_date = datetime(2024, m, day)
        order_date_str = order_date.strftime("%Y-%m-%d")
        delivery_days = random.randint(1, 10) if random.random() > 0.1 else None
        delivery_date = (order_date + timedelta(days=delivery_days)).strftime("%Y-%m-%d") if delivery_days else None
        status = random.choices(ORDER_STATUSES, weights=ORDER_STATUS_WEIGHTS)[0]
        payment_method = random.choices(PAYMENT_METHODS, weights=PAYMENT_WEIGHTS)[0]
        delivery_zone = random.choice(LOCATIONS)
        total_amount = round(random.uniform(500, 85000), 2)
        if random.random() < 0.2:
            total_amount = round(total_amount * random.uniform(1.5, 4), 2)  # Some outliers
        discount = round(random.uniform(0, 500), 2) if random.random() < 0.15 else 0
        rows.append((cust_id, order_date_str, delivery_date, status, payment_method, delivery_zone, total_amount, discount))
    return rows


def generate_order_items(order_ids, product_list, n_items=4500):
    """Generate order_items: 1-5 items per order, total ~4500."""
    result = []
    for _ in range(n_items):
        order_id = random.choice(order_ids)
        pid, unit_price = random.choice(product_list)
        qty = random.randint(1, 4)
        subtotal = round(qty * unit_price, 2)
        result.append((order_id, pid, qty, unit_price, subtotal))
    return result


def generate_payments(order_list):
    """One payment per order (order_id, total_amount, payment_method, order_date)."""
    payments = []
    for (oid, _, _, _, pm, _, total, _) in order_list:
        amount = total
        pay_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        ref = f"MP{random.randint(100000, 999999)}" if pm == "M-Pesa" else (f"TXN{random.randint(10000, 99999)}" if random.random() > 0.1 else None)
        status = "Completed" if random.random() > 0.02 else "Pending"
        payments.append((oid, pm, amount, pay_date, ref, status))
    return payments


def generate_support_tickets(customer_ids, n=300):
    """Generate 300 support tickets."""
    rows = []
    for i in range(n):
        cid = random.choice(customer_ids)
        issue = random.choice(ISSUE_TYPES)
        status = random.choices(SUPPORT_STATUSES, weights=[0.1, 0.85, 0.05])[0]
        created = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
        resolved = (datetime(2024, 1, 15) + timedelta(days=random.randint(0, 350))).strftime("%Y-%m-%d") if status != "Open" else None
        if random.random() < 0.05:
            satisfaction_score = None  # Some nulls for cleaning
        else:
            satisfaction_score = random.randint(1, 5)
        rows.append((cid, issue, status, created, resolved, satisfaction_score))
    return rows


def main():
    db_path = get_db_path()
    print(f"Creating database at {db_path}")
    conn = sqlite3.connect(db_path)

    run_schema(conn)

    # Customers
    print("Generating customers...")
    customers = generate_customers(500)
    conn.executemany(
        "INSERT INTO customers (first_name, last_name, email, phone, location, customer_type, registration_date, is_active) VALUES (?,?,?,?,?,?,?,?)",
        customers
    )
    customer_ids = [r[0] for r in conn.execute("SELECT customer_id FROM customers").fetchall()]
    print(f"  Inserted {len(customer_ids)} customers.")

    # Products
    print("Generating products...")
    products = generate_products()
    conn.executemany(
        "INSERT INTO products (product_name, category, unit_price, cost_price, stock_quantity, supplier, created_at) VALUES (?,?,?,?,?,?,?)",
        products
    )
    product_list = conn.execute("SELECT product_id, unit_price FROM products").fetchall()
    print(f"  Inserted {len(products)} products.")

    # Orders
    print("Generating orders...")
    orders = generate_orders(customer_ids, 2000)
    conn.executemany(
        "INSERT INTO orders (customer_id, order_date, delivery_date, status, payment_method, delivery_zone, total_amount, discount_applied) VALUES (?,?,?,?,?,?,?,?)",
        orders
    )
    order_ids = [r[0] for r in conn.execute("SELECT order_id FROM orders").fetchall()]
    order_list = conn.execute(
        "SELECT order_id, order_date, delivery_date, status, payment_method, delivery_zone, total_amount, discount_applied FROM orders"
    ).fetchall()
    print(f"  Inserted {len(orders)} orders.")

    # Order items
    print("Generating order items...")
    items = generate_order_items(order_ids, product_list, 4500)
    conn.executemany(
        "INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES (?,?,?,?,?)",
        items
    )
    print(f"  Inserted {len(items)} order items.")

    # Payments
    print("Generating payments...")
    payments = generate_payments(order_list)
    conn.executemany(
        "INSERT INTO payments (order_id, payment_method, amount_paid, payment_date, transaction_ref, status) VALUES (?,?,?,?,?,?)",
        payments
    )
    print(f"  Inserted {len(payments)} payments.")

    # Support
    print("Generating support tickets...")
    support = generate_support_tickets(customer_ids, 300)
    conn.executemany(
        "INSERT INTO customer_support (customer_id, issue_type, status, created_date, resolved_date, satisfaction_score) VALUES (?,?,?,?,?,?)",
        support
    )
    print(f"  Inserted {len(support)} support tickets.")

    conn.commit()

    # Summary
    print("\n--- Database summary ---")
    for table in ["customers", "products", "orders", "order_items", "payments", "customer_support"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()
    print("\nDone. Database ready at:", db_path)


if __name__ == "__main__":
    main()
