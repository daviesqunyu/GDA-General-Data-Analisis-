-- 04_subqueries.sql
-- Subqueries, nested queries, EXISTS
-- Nairobi Business Analytics

-- 1. Customers who spent more than the average customer spend
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    ROUND(SUM(o.total_amount), 2) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status NOT IN ('Cancelled', 'Returned')
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(o.total_amount) > (
    SELECT AVG(cust_total) FROM (
        SELECT SUM(total_amount) AS cust_total
        FROM orders
        WHERE status NOT IN ('Cancelled', 'Returned')
        GROUP BY customer_id
    )
)
ORDER BY total_spent DESC;

-- 2. Products whose price is above the category average price
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price,
    (SELECT ROUND(AVG(unit_price), 2) FROM products WHERE category = p.category) AS category_avg_price
FROM products p
WHERE p.unit_price > (
    SELECT AVG(unit_price) FROM products WHERE category = p.category
)
ORDER BY p.category, p.unit_price DESC;

-- 3. Orders placed by customers who have also raised support tickets
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount,
    o.status
FROM orders o
WHERE EXISTS (
    SELECT 1 FROM customer_support cs
    WHERE cs.customer_id = o.customer_id
)
AND o.status NOT IN ('Cancelled', 'Returned')
ORDER BY o.order_date DESC;

-- 4. Top 3 customers per location using subquery
SELECT 
    location,
    customer_id,
    first_name,
    last_name,
    total_spent,
    rn
FROM (
    SELECT 
        c.location,
        c.customer_id,
        c.first_name,
        c.last_name,
        ROUND(SUM(o.total_amount), 2) AS total_spent,
        ROW_NUMBER() OVER (PARTITION BY c.location ORDER BY SUM(o.total_amount) DESC) AS rn
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status NOT IN ('Cancelled', 'Returned')
    GROUP BY c.customer_id, c.first_name, c.last_name, c.location
)
WHERE rn <= 3
ORDER BY location, rn;

-- 5. Month with highest revenue
SELECT 
    month,
    total_revenue
FROM (
    SELECT 
        strftime('%Y-%m', order_date) AS month,
        SUM(total_amount) AS total_revenue
    FROM orders
    WHERE status NOT IN ('Cancelled', 'Returned')
      AND order_date >= '2024-01-01'
    GROUP BY strftime('%Y-%m', order_date)
)
ORDER BY total_revenue DESC
LIMIT 1;
