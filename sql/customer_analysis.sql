-- ============================================================
-- CUSTOMER ANALYSIS
-- ============================================================


-- ============================================================
-- 1. CUSTOMER OVERVIEW
-- ============================================================

SELECT

    customer_id,

    recency,

    frequency,

    monetary,

    average_order_value,

    customer_lifetime,

    total_quantity,

    unique_products,

    avg_purchase_interval,

    median_purchase_interval,

    weekend_purchase_ratio,

    avg_monthly_orders

FROM customer_features

ORDER BY monetary DESC;


-- ============================================================
-- 2. TOP 20 CUSTOMERS BY REVENUE
-- ============================================================

SELECT

    customer_id,

    monetary AS total_revenue,

    frequency AS total_orders,

    average_order_value,

    recency

FROM customer_features

ORDER BY monetary DESC

LIMIT 20;


-- ============================================================
-- 3. TOP CUSTOMERS BY ORDER FREQUENCY
-- ============================================================

SELECT

    customer_id,

    frequency AS total_orders,

    monetary AS revenue,

    average_order_value,

    recency

FROM customer_features

ORDER BY frequency DESC

LIMIT 20;


-- ============================================================
-- 4. TOP CUSTOMERS BY AVERAGE ORDER VALUE
-- ============================================================

SELECT

    customer_id,

    average_order_value,

    frequency,

    monetary

FROM customer_features

WHERE frequency > 0

ORDER BY average_order_value DESC

LIMIT 20;


-- ============================================================
-- 5. CUSTOMER REVENUE PERCENTILE
-- ============================================================

SELECT

    customer_id,

    monetary,

    NTILE(10) OVER (

        ORDER BY monetary DESC

    ) AS revenue_decile

FROM customer_features

ORDER BY monetary DESC;


-- ============================================================
-- 6. CUSTOMER VALUE RANKING
-- ============================================================

SELECT

    customer_id,

    monetary,

    frequency,

    recency,

    RANK() OVER (

        ORDER BY monetary DESC

    ) AS revenue_rank,

    RANK() OVER (

        ORDER BY frequency DESC

    ) AS frequency_rank,

    RANK() OVER (

        ORDER BY recency ASC

    ) AS recency_rank

FROM customer_features;


-- ============================================================
-- 7. CUSTOMER CONTRIBUTION TO TOTAL REVENUE
-- ============================================================

SELECT

    customer_id,

    monetary,

    ROUND(

        100.0 * monetary /

        NULLIF(

            SUM(monetary) OVER (),

            0

        ),

        2

    ) AS revenue_percentage

FROM customer_features

ORDER BY monetary DESC;


-- ============================================================
-- 8. CUMULATIVE REVENUE CONTRIBUTION
-- ============================================================

SELECT

    customer_id,

    monetary,

    ROUND(

        100.0 *

        SUM(monetary) OVER (

            ORDER BY monetary DESC

            ROWS BETWEEN UNBOUNDED PRECEDING

            AND CURRENT ROW

        )

        /

        NULLIF(

            SUM(monetary) OVER (),

            0

        ),

        2

    ) AS cumulative_revenue_percentage

FROM customer_features

ORDER BY monetary DESC;


-- ============================================================
-- 9. CUSTOMER ACTIVITY BY COUNTRY
-- ============================================================

SELECT

    t.country,

    COUNT(
        DISTINCT t.customer_id
    ) AS customers,

    COUNT(
        DISTINCT t.invoice_no
    ) AS orders,

    SUM(t.quantity)
        AS units,

    SUM(t.revenue)
        AS revenue

FROM transactions t

WHERE t.quantity > 0
  AND t.revenue > 0

GROUP BY t.country

ORDER BY revenue DESC;


-- ============================================================
-- 10. CUSTOMER PURCHASE BEHAVIOR
-- ============================================================

SELECT

    customer_id,

    recency,

    frequency,

    monetary,

    CASE

        WHEN recency <= 30
             AND frequency >= 10
             AND monetary >= 5000

            THEN 'Highly Active'

        WHEN recency <= 90
             AND frequency >= 5

            THEN 'Active'

        WHEN recency <= 180

            THEN 'At Risk'

        ELSE

            'Inactive'

    END AS customer_status

FROM customer_features

ORDER BY monetary DESC;


-- ============================================================
-- 11. MONTHLY CUSTOMER GROWTH
-- ============================================================

WITH first_purchase AS (

    SELECT

        customer_id,

        MIN(
            invoice_date
        ) AS first_purchase_date

    FROM transactions

    WHERE quantity > 0
      AND revenue > 0

    GROUP BY customer_id
)

SELECT

    DATE_TRUNC(
        'month',
        first_purchase_date
    ) AS acquisition_month,

    COUNT(*) AS new_customers

FROM first_purchase

GROUP BY

    DATE_TRUNC(
        'month',
        first_purchase_date
    )

ORDER BY acquisition_month;


-- ============================================================
-- 12. CUSTOMER ORDER TREND
-- ============================================================

SELECT

    DATE_TRUNC(
        'month',
        invoice_date
    ) AS month,

    COUNT(
        DISTINCT invoice_no
    ) AS orders,

    COUNT(
        DISTINCT customer_id
    ) AS active_customers,

    SUM(revenue) AS revenue

FROM transactions

WHERE quantity > 0
  AND revenue > 0

GROUP BY

    DATE_TRUNC(
        'month',
        invoice_date
    )

ORDER BY month;