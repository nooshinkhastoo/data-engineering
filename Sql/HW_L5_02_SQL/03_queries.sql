
/*==================================================
Question 1
==================================================*/

SELECT
    c.name AS customer_name,
    p.name AS product_name,
    o.quantity
FROM orders o
JOIN customers c
    ON o.customer_id = c.id
JOIN products p
    ON o.product_id = p.id;


/*==================================================
Question 2
==================================================*/

SELECT
    p.name AS product_name,
    COALESCE(SUM(o.quantity), 0) AS total_sales
FROM products p
LEFT JOIN orders o
    ON p.id = o.product_id
GROUP BY p.id, p.name
ORDER BY total_sales DESC;


/*==================================================
Question 3
==================================================*/

SELECT
    c.name AS customer_name,
    COUNT(o.id) AS order_count
FROM customers c
JOIN orders o
    ON c.id = o.customer_id
GROUP BY c.id, c.name
HAVING COUNT(o.id) > 2;


/*==================================================
Question 4
==================================================*/

SELECT
    id,
    name,
    price,
    stock,
    category
FROM products
ORDER BY price DESC
LIMIT 1;


/*==================================================
Question 5
==================================================*/

SELECT
    c.id,
    c.name,
    c.email,
    c.city,
    o.id AS order_id,
    o.quantity,
    o.order_date
FROM customers c
LEFT JOIN orders o
    ON c.id = o.customer_id
ORDER BY c.id;