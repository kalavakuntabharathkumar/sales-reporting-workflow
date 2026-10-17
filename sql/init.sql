CREATE TABLE IF NOT EXISTS sales_orders (
  order_id TEXT PRIMARY KEY,
  order_date DATE NOT NULL,
  region TEXT NOT NULL,
  product TEXT NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity >= 0),
  unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
  source TEXT NOT NULL DEFAULT 'postgres'
);
INSERT INTO sales_orders (order_id, order_date, region, product, quantity, unit_price, source)
VALUES
 ('SO-1001','2026-09-01','South','Cloud Plan',12,89.00,'postgres'),
 ('SO-1002','2026-09-02','West','Support Pack',7,120.00,'postgres'),
 ('SO-1003','2026-09-03','North','Cloud Plan',15,89.00,'postgres'),
 ('SO-1004','2026-09-04','East','Security Add-on',9,45.00,'postgres')
ON CONFLICT (order_id) DO NOTHING;
