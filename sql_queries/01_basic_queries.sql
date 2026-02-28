-- 01_basic_queries.sql
-- Basic SELECT, WHERE, ORDER BY, LIMIT
-- Nairobi Business Analytics

-- 1. List all customers in Westlands ordered by registration date
SELECT customer_id, first_name, last_name, email, location, registration_date
FROM customers
WHERE location = 'Westlands'
ORDER BY registration_date;

-- 2. Find all products with stock below 10 units
SELECT product_id, product_name, category, stock_quantity, unit_price
FROM products
WHERE stock_quantity < 10
ORDER BY stock_quantity ASC;

-- 3. Show all orders placed in November and December 2024
SELECT order_id, customer_id, order_date, status, total_amount, payment_method
FROM orders
WHERE order_date >= '2024-11-01' AND order_date <= '2024-12-31'
ORDER BY order_date;

-- 4. Find cancelled and returned orders
SELECT order_id, customer_id, order_date, status, total_amount
FROM orders
WHERE status IN ('Cancelled', 'Returned')
ORDER BY order_date DESC;

-- 5. List top 10 most expensive products
SELECT product_id, product_name, category, unit_price, stock_quantity
FROM products
ORDER BY unit_price DESC
LIMIT 10;
