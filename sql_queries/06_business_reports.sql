-- 06_business_reports.sql
-- KPI reports: revenue, churn, top customers, delivery performance
-- Nairobi Business Analytics

-- 1. Monthly Revenue Report — revenue, order count, avg order value, by month
SELECT 
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS order_count,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE status NOT IN ('Cancelled', 'Returned')
  AND order_date >= '2024-01-01' AND order_date <= '2024-12-31'
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;

-- 2. Customer Lifetime Value (CLV) — total spend per customer since registration
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.registration_date,
    c.customer_type,
    COUNT(o.order_id) AS order_count,
    ROUND(COALESCE(SUM(o.total_amount), 0), 2) AS lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status NOT IN ('Cancelled', 'Returned')
GROUP BY c.customer_id, c.first_name, c.last_name, c.registration_date, c.customer_type
ORDER BY lifetime_value DESC;

-- 3. Top 20 Customers by Revenue
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.location,
    c.customer_type,
    COUNT(o.order_id) AS order_count,
    ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status NOT IN ('Cancelled', 'Returned')
GROUP BY c.customer_id, c.first_name, c.last_name, c.location, c.customer_type
ORDER BY total_revenue DESC
LIMIT 20;

-- 4. Product Performance Report — units sold, revenue, profit margin per product
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.subtotal), 2) AS revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.cost_price)), 2) AS profit,
    ROUND(100.0 * SUM(oi.quantity * (oi.unit_price - p.cost_price)) / NULLIF(SUM(oi.subtotal), 0), 2) AS profit_margin_pct
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status NOT IN ('Cancelled', 'Returned')
GROUP BY p.product_id, p.product_name, p.category
ORDER BY revenue DESC;

-- 5. Payment Method Analysis — which payment method drives most revenue
SELECT 
    payment_method,
    COUNT(*) AS transaction_count,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_transaction_value
FROM orders
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY payment_method
ORDER BY total_revenue DESC;

-- 6. Delivery Performance — average days between order and delivery by zone
SELECT 
    delivery_zone,
    COUNT(*) AS orders_delivered,
    ROUND(AVG(
        JULIANDAY(delivery_date) - JULIANDAY(order_date)
    ), 2) AS avg_delivery_days
FROM orders
WHERE status = 'Delivered'
  AND delivery_date IS NOT NULL
  AND order_date IS NOT NULL
GROUP BY delivery_zone
ORDER BY avg_delivery_days;

-- 7. Churn Report — customers who ordered in H1 2024 but NOT in H2 2024
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.location,
    ROUND(SUM(o.total_amount), 2) AS h1_revenue,
    COUNT(o.order_id) AS h1_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
    AND o.order_date >= '2024-01-01' AND o.order_date <= '2024-06-30'
    AND o.status NOT IN ('Cancelled', 'Returned')
WHERE c.customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE order_date >= '2024-07-01' AND order_date <= '2024-12-31'
      AND status NOT IN ('Cancelled', 'Returned')
)
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.location
ORDER BY h1_revenue DESC;
