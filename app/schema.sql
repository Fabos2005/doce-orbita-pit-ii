PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL CHECK(length(name) BETWEEN 2 AND 80),
 email TEXT NOT NULL COLLATE NOCASE UNIQUE CHECK(length(email) BETWEEN 5 AND 160),
 password_hash TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS products (
 id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE CHECK(length(name) BETWEEN 2 AND 100),
 description TEXT NOT NULL CHECK(length(description)<=500),
 flavor TEXT NOT NULL CHECK(length(flavor)<=50), allergens TEXT NOT NULL,
 price_cents INTEGER NOT NULL CHECK(price_cents BETWEEN 1 AND 100000),
 stock INTEGER NOT NULL CHECK(stock BETWEEN 0 AND 9999),
 active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)));
CREATE TABLE IF NOT EXISTS orders (
 id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id),
 request_key TEXT NOT NULL UNIQUE, status TEXT NOT NULL DEFAULT 'aguardando pagamento'
 CHECK(status IN ('aguardando pagamento','confirmado','em preparo','saiu para entrega','entregue','cancelado')),
 recipient TEXT NOT NULL, street TEXT NOT NULL, number TEXT NOT NULL, complement TEXT NOT NULL DEFAULT '',
 district TEXT NOT NULL, city TEXT NOT NULL, state TEXT NOT NULL, postal_code TEXT NOT NULL,
 delivery_cents INTEGER NOT NULL CHECK(delivery_cents>=0),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS order_items (
 order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id),
 product_name TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity BETWEEN 1 AND 99),
 unit_cents INTEGER NOT NULL CHECK(unit_cents>0), PRIMARY KEY(order_id,product_id));
CREATE TABLE IF NOT EXISTS payments (
 id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(id),
 method TEXT NOT NULL CHECK(method IN ('pix','cartao')),
 result TEXT NOT NULL CHECK(result IN ('aprovado','recusado')),
 amount_cents INTEGER NOT NULL CHECK(amount_cents>0),
 simulation INTEGER NOT NULL DEFAULT 1 CHECK(simulation=1), created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE UNIQUE INDEX IF NOT EXISTS one_approved_payment ON payments(order_id) WHERE result='aprovado';
CREATE INDEX IF NOT EXISTS orders_customer ON orders(user_id,created_at);
CREATE INDEX IF NOT EXISTS orders_status ON orders(status);
CREATE TABLE IF NOT EXISTS order_events (
 id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(id),
 status TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
