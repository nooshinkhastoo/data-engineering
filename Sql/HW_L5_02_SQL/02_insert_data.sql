INSERT INTO customers (name, email, city) VALUES
('Ali Ahmadi', 'ali@gmail.com', 'Tehran'),
('Sara Mohammadi', 'sara@gmail.com', 'Shiraz'),
('Reza Karimi', 'reza@gmail.com', 'Tabriz'),
('Maryam Hosseini', 'maryam@gmail.com', 'Mashhad'),
('Nima Jafari', 'nima@gmail.com', 'Isfahan');

INSERT INTO products (name, price, stock, category) VALUES
('Laptop', 1200.00, 15, 'Electronics'),
('Keyboard', 50.00, 100, 'Electronics'),
('Mouse', 30.00, 120, 'Electronics'),
('Headphone', 80.00, 50, 'Accessories'),
('Monitor', 300.00, 25, 'Electronics'),
('Office Chair', 200.00, 20, 'Furniture');

INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
(1, 1, 1, '2025-06-01'),
(1, 2, 2, '2025-06-02'),
(2, 3, 3, '2025-06-02'),
(3, 1, 1, '2025-06-03'),
(2, 4, 2, '2025-06-04'),
(4, 5, 1, '2025-06-05'),
(1, 3, 4, '2025-06-05'),
(5, 6, 1, '2025-06-06'),
(3, 2, 2, '2025-06-07'),
(2, 5, 1, '2025-06-08');