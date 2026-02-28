-- 02_aggregations.sql
-- GROUP BY, HAVING, COUNT, SUM, AVG, MIN, MAX
-- Nairobi Business Analytics

-- 1. Total revenue by month for 2024
SELECT 
    strftime('%Y-%m', order_date) AS month,
    SUM(total_amount) AS total_revenue,
    COUNT(*) AS order_count
FROM orders
WHERE status NOT IN ('Cancelled', 'Returned')
  AND order_date >= '2024-01-01' AND order_date <= '2024-12-31'
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;

-- 2. Average order value by customer type (Individual/SME/Corporate)
SELECT 
    c.customer_type,
    COUNT(o.order_id) AS order_count,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status NOT IN ('Cancelled', 'Returned')
GROUP BY c.customer_type
ORDER BY avg_order_value DESC;

-- 3. Number of orders by payment method
SELECT 
    payment_method,
    COUNT(*) AS order_count,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM orders
WHERE status NOT IN ('Cancelled', 'Returned')
GROUP BY payment_method
ORDER BY order_count DESC;

-- 4. Total revenue by product category
SELECT 
    p.category,
    COUNT(oi.item_id) AS items_sold,
    ROUND(SUM(oi.subtotal), 2) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status NOT IN ('Cancelled', 'Returned')
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 5. Count of customers by location/neighbourhood
SELECT 
    location,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) AS active_count
FROM customers
GROUP BY location
ORDER BY customer_count DESC;

-- 6. Average satisfaction score by issue type
SELECT 
    issue_type,
    COUNT(*) AS ticket_count,
    ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction_score
FROM customer_support
WHERE satisfaction_score IS NOT NULL
GROUP BY issue_type
ORDER BY avg_satisfaction_score DESC;
