-- 07_advanced_analytics.sql
-- Cohort analysis, RFM segmentation, basket analysis
-- Nairobi Business Analytics

-- 1. RFM Segmentation — Recency, Frequency, Monetary (raw values; scoring 1-5 done in Python)
WITH rfm_raw AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        CAST(JULIANDAY('2024-12-31') - JULIANDAY(MAX(o.order_date)) AS INTEGER) AS recency_days,
        COUNT(o.order_id) AS frequency,
        ROUND(SUM(o.total_amount), 2) AS monetary
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status NOT IN ('Cancelled', 'Returned')
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT 
    customer_id,
    first_name,
    last_name,
    recency_days,
    frequency,
    monetary
FROM rfm_raw
ORDER BY monetary DESC;

-- 2. Cohort Analysis — customers by registration month, orders in subsequent months
WITH cohort AS (
    SELECT 
        customer_id,
        strftime('%Y-%m', MIN(registration_date)) AS cohort_month
    FROM customers
    WHERE registration_date >= '2024-01-01'
    GROUP BY customer_id
),
order_months AS (
    SELECT 
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o
    WHERE o.status NOT IN ('Cancelled', 'Returned')
      AND o.order_date >= '2024-01-01'
    GROUP BY o.customer_id, strftime('%Y-%m', o.order_date)
)
SELECT 
    c.cohort_month,
    om.order_month,
    COUNT(DISTINCT om.customer_id) AS customers_with_orders
FROM cohort c
JOIN order_months om ON c.customer_id = om.customer_id
WHERE om.order_month >= c.cohort_month
GROUP BY c.cohort_month, om.order_month
ORDER BY c.cohort_month, om.order_month;

-- 3. Category Revenue Trend — monthly revenue per product category (CASE WHEN pivot)
SELECT 
    strftime('%Y-%m', o.order_date) AS month,
    ROUND(SUM(CASE WHEN p.category = 'Electronics' THEN oi.subtotal ELSE 0 END), 2) AS Electronics,
    ROUND(SUM(CASE WHEN p.category = 'Clothing' THEN oi.subtotal ELSE 0 END), 2) AS Clothing,
    ROUND(SUM(CASE WHEN p.category = 'Food' THEN oi.subtotal ELSE 0 END), 2) AS Food,
    ROUND(SUM(CASE WHEN p.category = 'Home' THEN oi.subtotal ELSE 0 END), 2) AS Home,
    ROUND(SUM(CASE WHEN p.category = 'Beauty' THEN oi.subtotal ELSE 0 END), 2) AS Beauty,
    ROUND(SUM(CASE WHEN p.category = 'Sports' THEN oi.subtotal ELSE 0 END), 2) AS Sports,
    ROUND(SUM(oi.subtotal), 2) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status NOT IN ('Cancelled', 'Returned')
  AND o.order_date >= '2024-01-01' AND o.order_date <= '2024-12-31'
GROUP BY strftime('%Y-%m', o.order_date)
ORDER BY month;

-- 4. Repeat vs New Customer Revenue — first-time vs returning per month
WITH first_order AS (
    SELECT 
        customer_id,
        MIN(order_date) AS first_order_date
    FROM orders
    WHERE status NOT IN ('Cancelled', 'Returned')
    GROUP BY customer_id
)
SELECT 
    strftime('%Y-%m', o.order_date) AS month,
    ROUND(SUM(CASE WHEN o.order_date = fo.first_order_date THEN o.total_amount ELSE 0 END), 2) AS new_customer_revenue,
    ROUND(SUM(CASE WHEN o.order_date > fo.first_order_date THEN o.total_amount ELSE 0 END), 2) AS repeat_customer_revenue,
    ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM orders o
JOIN first_order fo ON o.customer_id = fo.customer_id
WHERE o.status NOT IN ('Cancelled', 'Returned')
  AND o.order_date >= '2024-01-01' AND o.order_date <= '2024-12-31'
GROUP BY strftime('%Y-%m', o.order_date)
ORDER BY month;

-- 5. Basket Analysis — most commonly purchased product combinations (pairs)
WITH order_products AS (
    SELECT 
        oi.order_id,
        oi.product_id,
        p.product_name
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status NOT IN ('Cancelled', 'Returned')
),
pairs AS (
    SELECT 
        a.product_id AS product_a_id,
        b.product_id AS product_b_id,
        a.product_name AS product_a,
        b.product_name AS product_b
    FROM order_products a
    JOIN order_products b ON a.order_id = b.order_id AND a.product_id < b.product_id
)
SELECT 
    product_a,
    product_b,
    COUNT(*) AS times_bought_together
FROM pairs
GROUP BY product_a_id, product_b_id, product_a, product_b
ORDER BY times_bought_together DESC
LIMIT 20;
