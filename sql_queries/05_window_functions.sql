-- 05_window_functions.sql
-- ROW_NUMBER, RANK, LAG, LEAD, running totals
-- Nairobi Business Analytics

-- 1. Rank customers by total spend (RANK, DENSE_RANK)
SELECT 
    customer_id,
    first_name,
    last_name,
    total_spent,
    RANK() OVER (ORDER BY total_spent DESC) AS rank_spend,
    DENSE_RANK() OVER (ORDER BY total_spent DESC) AS dense_rank_spend
FROM (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        ROUND(SUM(o.total_amount), 2) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status NOT IN ('Cancelled', 'Returned')
    GROUP BY c.customer_id, c.first_name, c.last_name
);

-- 2. Running total of monthly revenue (SUM OVER)
SELECT 
    month,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (ORDER BY month), 2) AS running_total
FROM (
    SELECT 
        strftime('%Y-%m', order_date) AS month,
        SUM(total_amount) AS monthly_revenue
    FROM orders
    WHERE status NOT IN ('Cancelled', 'Returned')
      AND order_date >= '2024-01-01' AND order_date <= '2024-12-31'
    GROUP BY strftime('%Y-%m', order_date)
)
ORDER BY month;

-- 3. Month-over-month revenue change (LAG)
SELECT 
    month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month), 2) AS mom_change
FROM (
    SELECT 
        strftime('%Y-%m', order_date) AS month,
        SUM(total_amount) AS monthly_revenue
    FROM orders
    WHERE status NOT IN ('Cancelled', 'Returned')
      AND order_date >= '2024-01-01' AND order_date <= '2024-12-31'
    GROUP BY strftime('%Y-%m', order_date)
)
ORDER BY month;

-- 4. Row number per customer ordered by order date (ROW_NUMBER PARTITION BY)
SELECT 
    customer_id,
    order_id,
    order_date,
    total_amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_sequence
FROM orders
WHERE status NOT IN ('Cancelled', 'Returned')
ORDER BY customer_id, order_date;

-- 5. 3-month moving average of sales (window frame)
SELECT 
    month,
    monthly_revenue,
    ROUND(AVG(monthly_revenue) OVER (
        ORDER BY month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_3m
FROM (
    SELECT 
        strftime('%Y-%m', order_date) AS month,
        SUM(total_amount) AS monthly_revenue
    FROM orders
    WHERE status NOT IN ('Cancelled', 'Returned')
      AND order_date >= '2024-01-01' AND order_date <= '2024-12-31'
    GROUP BY strftime('%Y-%m', order_date)
)
ORDER BY month;
