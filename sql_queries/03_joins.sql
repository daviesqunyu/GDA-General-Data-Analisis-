-- 03_joins.sql
-- INNER JOIN, LEFT JOIN, multiple table joins
-- Nairobi Business Analytics

-- 1. Customer name + all their orders (INNER JOIN)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    o.order_id,
    o.order_date,
    o.status,
    o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_date;

-- 2. All customers including those with no orders (LEFT JOIN)
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.location,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status NOT IN ('Cancelled', 'Returned')
GROUP BY c.customer_id, c.first_name, c.last_name, c.location
ORDER BY total_spent DESC;

-- 3. Full order details: customer + order + items + product names (4-table JOIN)
SELECT 
    c.first_name,
    c.last_name,
    o.order_id,
    o.order_date,
    o.status,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    oi.subtotal
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status NOT IN ('Cancelled', 'Returned')
ORDER BY o.order_id, oi.item_id;

-- 4. Revenue per customer with customer details
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
ORDER BY total_revenue DESC;

-- 5. Products that have never been ordered
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price,
    p.stock_quantity
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.item_id IS NULL
ORDER BY p.product_id;
