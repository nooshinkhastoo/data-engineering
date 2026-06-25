-- ==========================================
-- 1
-- ==========================================
SELECT
    c.name AS category_name,
    COUNT(DISTINCT p.id) AS product_count,
    COALESCE(SUM(oi.quantity), 0) AS total_sold,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue
FROM categories c
JOIN products p
    ON p.category_id = c.id
LEFT JOIN order_items oi
    ON oi.product_id = p.id
GROUP BY c.id, c.name
HAVING COALESCE(SUM(oi.quantity), 0) >= 5;


-- ==========================================
-- 2
-- ==========================================
WITH ranked_inventory AS (
    SELECT
        w.name AS warehouse_name,
        p.name AS product_name,
        i.quantity,
        RANK() OVER (
            PARTITION BY w.id
            ORDER BY i.quantity DESC
        ) AS product_rank
    FROM inventory i
    JOIN warehouses w
        ON w.id = i.warehouse_id
    JOIN products p
        ON p.id = i.product_id
)
SELECT
    warehouse_name,
    product_name,
    quantity,
    product_rank
FROM ranked_inventory
WHERE product_rank <= 3;


-- ==========================================
-- 3
-- ==========================================
WITH customer_stats AS (
    SELECT
        c.id,
        c.full_name,
        SUM(oi.quantity * oi.unit_price) AS total_spent,
        COUNT(DISTINCT o.id) AS order_count
    FROM customers c
    JOIN orders o
        ON o.customer_id = c.id
    JOIN order_items oi
        ON oi.order_id = o.id
    GROUP BY c.id, c.full_name
),
average_spending AS (
    SELECT AVG(total_spent) AS avg_spent
    FROM customer_stats
)
SELECT
    cs.full_name,
    cs.total_spent,
    cs.order_count,
    cs.total_spent / NULLIF(cs.order_count, 0) AS avg_order_value
FROM customer_stats cs
CROSS JOIN average_spending a
WHERE cs.total_spent > a.avg_spent;


-- ==========================================
-- 4
-- ==========================================
WITH product_stats AS (
    SELECT
        p.id,
        p.name,
        COALESCE(SUM(oi.quantity), 0) AS total_sales,
        COALESCE(SUM(i.quantity), 0) AS total_inventory
    FROM products p
    LEFT JOIN order_items oi
        ON oi.product_id = p.id
    LEFT JOIN inventory i
        ON i.product_id = p.id
    GROUP BY p.id, p.name
),
ranked_products AS (
    SELECT
        *,
        total_sales::DECIMAL / NULLIF(total_inventory, 0) AS sales_inventory_ratio,
        PERCENT_RANK() OVER (
            ORDER BY total_sales::DECIMAL / NULLIF(total_inventory, 0)
        ) AS percentile_rank
    FROM product_stats
)
SELECT
    name,
    total_sales,
    total_inventory,
    sales_inventory_ratio
FROM ranked_products
WHERE percentile_rank >= 0.8;