-- Nairobi Business Intelligence & Sales Analytics System
-- Database Schema for SQLite
-- Author: Davis Kunyu Wamalwa

-- Drop tables if they exist (for clean re-run)
DROP TABLE IF EXISTS customer_support;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Table 1: customers
CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT UNIQUE NOT NULL,
    phone           TEXT,
    location        TEXT,
    customer_type   TEXT,
    registration_date DATE,
    is_active       INTEGER DEFAULT 1
);

CREATE INDEX idx_customers_location ON customers(location);
CREATE INDEX idx_customers_type ON customers(customer_type);
CREATE INDEX idx_customers_registration ON customers(registration_date);

-- Table 2: products
CREATE TABLE products (
    product_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name    TEXT NOT NULL,
    category        TEXT,
    unit_price      REAL NOT NULL,
    cost_price      REAL NOT NULL,
    stock_quantity  INTEGER,
    supplier        TEXT,
    created_at      DATE
);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_price ON products(unit_price);

-- Table 3: orders
CREATE TABLE orders (
    order_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id     INTEGER NOT NULL,
    order_date      DATE NOT NULL,
    delivery_date   DATE,
    status          TEXT,
    payment_method  TEXT,
    delivery_zone   TEXT,
    total_amount    REAL,
    discount_applied REAL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);

-- Table 4: order_items
CREATE TABLE order_items (
    item_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    quantity        INTEGER NOT NULL,
    unit_price      REAL NOT NULL,
    subtotal        REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- Table 5: payments
CREATE TABLE payments (
    payment_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        INTEGER NOT NULL,
    payment_method  TEXT,
    amount_paid     REAL,
    payment_date    DATE,
    transaction_ref TEXT,
    status          TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE INDEX idx_payments_order ON payments(order_id);

-- Table 6: customer_support
CREATE TABLE customer_support (
    ticket_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id         INTEGER NOT NULL,
    issue_type          TEXT,
    status              TEXT,
    created_date        DATE,
    resolved_date       DATE,
    satisfaction_score  INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX idx_support_customer ON customer_support(customer_id);
CREATE INDEX idx_support_issue ON customer_support(issue_type);
