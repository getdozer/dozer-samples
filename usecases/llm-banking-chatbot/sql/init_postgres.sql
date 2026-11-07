-- Initialize PostgreSQL tables for Dozer CDC Banking Chatbot Sample
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_code VARCHAR(16) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    age INT NOT NULL,
    annual_income DOUBLE PRECISION NOT NULL,
    credit_score INT NOT NULL,
    employment_status VARCHAR(64) NOT NULL,
    preferred_reward_type VARCHAR(64) NOT NULL,
    city VARCHAR(64) NOT NULL
);

CREATE TABLE credit_accounts (
    account_id INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    existing_card_type VARCHAR(120) NOT NULL,
    current_balance DOUBLE PRECISION NOT NULL,
    credit_limit DOUBLE PRECISION NOT NULL,
    current_apr DOUBLE PRECISION NOT NULL,
    late_payments_last_year INT NOT NULL,
    account_age_months INT NOT NULL
);

CREATE TABLE transactions (
    tx_id INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    tx_date VARCHAR(32) NOT NULL,
    merchant VARCHAR(120) NOT NULL,
    category VARCHAR(64) NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    currency VARCHAR(16) NOT NULL,
    is_international BOOLEAN NOT NULL
);

CREATE TABLE card_products (
    product_id VARCHAR(16) PRIMARY KEY,
    card_name VARCHAR(120) NOT NULL,
    target_segment VARCHAR(64) NOT NULL,
    min_credit_score INT NOT NULL,
    min_annual_income DOUBLE PRECISION NOT NULL,
    annual_fee DOUBLE PRECISION NOT NULL,
    apr_range VARCHAR(64) NOT NULL,
    signup_bonus TEXT NOT NULL,
    primary_rewards TEXT NOT NULL,
    foreign_tx_fee_pct DOUBLE PRECISION NOT NULL,
    description TEXT NOT NULL
);

COPY customers FROM '/data/customers.csv' WITH (FORMAT csv, HEADER true);
COPY credit_accounts FROM '/data/credit_accounts.csv' WITH (FORMAT csv, HEADER true);
COPY transactions FROM '/data/transactions.csv' WITH (FORMAT csv, HEADER true);
COPY card_products FROM '/data/card_products.csv' WITH (FORMAT csv, HEADER true);
