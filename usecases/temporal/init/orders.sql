DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    customer UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    fulfilled_at TIMESTAMPTZ
);

CREATE TABLE order_items(
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    order_id UUID NOT NULL REFERENCES orders(id),
    item_id TEXT NOT NULL,
    amount INTEGER NOT NULL,
    price NUMERIC(8,2) NOT NULL
);
