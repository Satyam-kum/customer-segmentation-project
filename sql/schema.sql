-- ============================================================
-- CUSTOMER INTELLIGENCE PLATFORM
-- DATABASE SCHEMA
-- PostgreSQL
-- ============================================================


-- ============================================================
-- 1. TRANSACTIONS
-- ============================================================

DROP TABLE IF EXISTS transactions CASCADE;

CREATE TABLE transactions (

    transaction_id BIGSERIAL PRIMARY KEY,

    invoice_no VARCHAR(50),

    stock_code VARCHAR(50),

    description TEXT,

    quantity INTEGER,

    invoice_date TIMESTAMP,

    unit_price NUMERIC(12, 4),

    customer_id VARCHAR(50),

    country VARCHAR(100),

    revenue NUMERIC(14, 2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- INDEXES FOR TRANSACTIONS
-- ============================================================

CREATE INDEX idx_transactions_customer
ON transactions(customer_id);

CREATE INDEX idx_transactions_invoice_date
ON transactions(invoice_date);

CREATE INDEX idx_transactions_stock_code
ON transactions(stock_code);

CREATE INDEX idx_transactions_country
ON transactions(country);

CREATE INDEX idx_transactions_invoice_no
ON transactions(invoice_no);


-- ============================================================
-- 2. CUSTOMER FEATURES
-- ============================================================

DROP TABLE IF EXISTS customer_features CASCADE;

CREATE TABLE customer_features (

    customer_id VARCHAR(50) PRIMARY KEY,

    recency NUMERIC(14, 4),

    frequency NUMERIC(14, 4),

    monetary NUMERIC(14, 2),

    average_order_value NUMERIC(14, 2),

    customer_lifetime NUMERIC(14, 4),

    total_quantity NUMERIC(14, 4),

    unique_products INTEGER,

    avg_purchase_interval NUMERIC(14, 4),

    median_purchase_interval NUMERIC(14, 4),

    weekend_purchase_ratio NUMERIC(8, 4),

    avg_monthly_orders NUMERIC(14, 4),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 3. CUSTOMER SEGMENTS
-- ============================================================

DROP TABLE IF EXISTS customer_segments CASCADE;

CREATE TABLE customer_segments (

    customer_id VARCHAR(50) PRIMARY KEY,

    recency_score INTEGER,

    frequency_score INTEGER,

    monetary_score INTEGER,

    rfm_score VARCHAR(10),

    segment VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_segment_customer

        FOREIGN KEY(customer_id)

        REFERENCES customer_features(customer_id)

        ON DELETE CASCADE
);


-- ============================================================
-- 4. CHURN PREDICTIONS
-- ============================================================

DROP TABLE IF EXISTS churn_predictions CASCADE;

CREATE TABLE churn_predictions (

    customer_id VARCHAR(50) PRIMARY KEY,

    recency NUMERIC(14, 4),

    frequency NUMERIC(14, 4),

    monetary NUMERIC(14, 2),

    average_order_value NUMERIC(14, 2),

    churn_probability NUMERIC(8, 6),

    prediction INTEGER,

    churn_risk VARCHAR(20),

    retention_action VARCHAR(100),

    model_name VARCHAR(100),

    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_churn_customer

        FOREIGN KEY(customer_id)

        REFERENCES customer_features(customer_id)

        ON DELETE CASCADE
);


-- ============================================================
-- 5. MODEL RESULTS
-- ============================================================

DROP TABLE IF EXISTS churn_model_results CASCADE;

CREATE TABLE churn_model_results (

    model_name VARCHAR(100) PRIMARY KEY,

    accuracy NUMERIC(8, 6),

    precision_score NUMERIC(8, 6),

    recall NUMERIC(8, 6),

    f1 NUMERIC(8, 6),

    roc_auc NUMERIC(8, 6),

    pr_auc NUMERIC(8, 6),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 6. PRODUCTS
-- ============================================================

DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE products (

    stock_code VARCHAR(50) PRIMARY KEY,

    description TEXT,

    total_quantity BIGINT DEFAULT 0,

    total_revenue NUMERIC(14, 2) DEFAULT 0,

    unique_customers INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 7. CUSTOMER SUMMARY VIEW
-- ============================================================

CREATE OR REPLACE VIEW customer_summary AS

SELECT

    cf.customer_id,

    cf.recency,

    cf.frequency,

    cf.monetary,

    cf.average_order_value,

    cf.customer_lifetime,

    cf.total_quantity,

    cf.unique_products,

    cf.avg_purchase_interval,

    cf.median_purchase_interval,

    cf.weekend_purchase_ratio,

    cf.avg_monthly_orders,

    cs.segment,

    cs.rfm_score,

    cp.churn_probability,

    cp.churn_risk,

    cp.retention_action

FROM customer_features cf

LEFT JOIN customer_segments cs

    ON cf.customer_id = cs.customer_id

LEFT JOIN churn_predictions cp

    ON cf.customer_id = cp.customer_id;


-- ============================================================
-- 8. REVENUE SUMMARY VIEW
-- ============================================================

CREATE OR REPLACE VIEW revenue_summary AS

SELECT

    COUNT(DISTINCT customer_id)
        AS total_customers,

    COUNT(DISTINCT invoice_no)
        AS total_orders,

    SUM(quantity)
        AS total_units,

    SUM(revenue)
        AS total_revenue,

    AVG(revenue)
        AS average_transaction_value,

    MIN(invoice_date)
        AS first_transaction_date,

    MAX(invoice_date)
        AS last_transaction_date

FROM transactions
WHERE quantity > 0
  AND revenue > 0;


-- ============================================================
-- 9. MONTHLY REVENUE VIEW
-- ============================================================

CREATE OR REPLACE VIEW monthly_revenue AS

SELECT

    DATE_TRUNC(
        'month',
        invoice_date
    ) AS month,

    COUNT(DISTINCT invoice_no)
        AS orders,

    COUNT(DISTINCT customer_id)
        AS customers,

    SUM(quantity)
        AS units_sold,

    SUM(revenue)
        AS revenue

FROM transactions

WHERE quantity > 0
  AND revenue > 0

GROUP BY

    DATE_TRUNC(
        'month',
        invoice_date
    )

ORDER BY month;


-- ============================================================
-- 10. MONTHLY CUSTOMER ACTIVITY VIEW
-- ============================================================

CREATE OR REPLACE VIEW monthly_customer_activity AS

SELECT

    DATE_TRUNC(
        'month',
        invoice_date
    ) AS month,

    customer_id,

    COUNT(DISTINCT invoice_no)
        AS orders,

    SUM(quantity)
        AS quantity,

    SUM(revenue)
        AS revenue

FROM transactions

WHERE quantity > 0
  AND revenue > 0

GROUP BY

    DATE_TRUNC(
        'month',
        invoice_date
    ),

    customer_id;


-- ============================================================
-- SCHEMA COMPLETE
-- ============================================================