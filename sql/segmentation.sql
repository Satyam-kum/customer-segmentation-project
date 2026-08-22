-- ============================================================
-- CUSTOMER SEGMENTATION ANALYSIS
-- ============================================================


-- ============================================================
-- 1. SEGMENT OVERVIEW
-- ============================================================

SELECT

    segment,

    COUNT(*) AS customers,

    SUM(
        cf.monetary
    ) AS total_revenue,

    AVG(
        cf.monetary
    ) AS average_customer_value,

    AVG(
        cf.frequency
    ) AS average_frequency,

    AVG(
        cf.recency
    ) AS average_recency,

    AVG(
        cf.average_order_value
    ) AS average_order_value

FROM customer_segments cs

JOIN customer_features cf

    ON cs.customer_id = cf.customer_id

GROUP BY segment

ORDER BY total_revenue DESC;


-- ============================================================
-- 2. CUSTOMER COUNT BY SEGMENT
-- ============================================================

SELECT

    segment,

    COUNT(*) AS customer_count,

    ROUND(

        100.0 * COUNT(*)

        /

        SUM(COUNT(*)) OVER (),

        2

    ) AS customer_percentage

FROM customer_segments

GROUP BY segment

ORDER BY customer_count DESC;


-- ============================================================
-- 3. REVENUE CONTRIBUTION BY SEGMENT
-- ============================================================

SELECT

    cs.segment,

    SUM(
        cf.monetary
    ) AS revenue,

    ROUND(

        100.0 *

        SUM(cf.monetary)

        /

        SUM(
            SUM(cf.monetary)
        ) OVER (),

        2

    ) AS revenue_percentage

FROM customer_segments cs

JOIN customer_features cf

    ON cs.customer_id = cf.customer_id

GROUP BY cs.segment

ORDER BY revenue DESC;


-- ============================================================
-- 4. RFM SCORE DISTRIBUTION
-- ============================================================

SELECT

    rfm_score,

    COUNT(*) AS customers,

    AVG(
        cf.monetary
    ) AS average_revenue,

    AVG(
        cf.frequency
    ) AS average_frequency,

    AVG(
        cf.recency
    ) AS average_recency

FROM customer_segments cs

JOIN customer_features cf

    ON cs.customer_id = cf.customer_id

GROUP BY rfm_score

ORDER BY rfm_score DESC;


-- ============================================================
-- 5. TOP CUSTOMERS IN EACH SEGMENT
-- ============================================================

WITH ranked_customers AS (

    SELECT

        cs.segment,

        cs.customer_id,

        cf.monetary,

        cf.frequency,

        cf.recency,

        ROW_NUMBER() OVER (

            PARTITION BY cs.segment

            ORDER BY cf.monetary DESC

        ) AS rank

    FROM customer_segments cs

    JOIN customer_features cf

        ON cs.customer_id =
           cf.customer_id
)

SELECT

    segment,

    customer_id,

    monetary,

    frequency,

    recency

FROM ranked_customers

WHERE rank <= 10

ORDER BY

    segment,

    monetary DESC;


-- ============================================================
-- 6. SEGMENT + CHURN RISK
-- ============================================================

SELECT

    cs.segment,

    cp.churn_risk,

    COUNT(*) AS customers,

    SUM(
        cp.monetary
    ) AS revenue

FROM customer_segments cs

JOIN churn_predictions cp

    ON cs.customer_id = cp.customer_id

GROUP BY

    cs.segment,

    cp.churn_risk

ORDER BY

    cs.segment,

    revenue DESC;


-- ============================================================
-- 7. SEGMENT CHURN SUMMARY
-- ============================================================

SELECT

    cs.segment,

    COUNT(*) AS customers,

    AVG(
        cp.churn_probability
    ) AS average_churn_probability,

    SUM(
        CASE
            WHEN cp.churn_risk = 'HIGH'
            THEN 1
            ELSE 0
        END
    ) AS high_risk_customers,

    SUM(
        CASE
            WHEN cp.churn_risk = 'HIGH'
            THEN cp.monetary
            ELSE 0
        END
    ) AS revenue_at_risk

FROM customer_segments cs

LEFT JOIN churn_predictions cp

    ON cs.customer_id = cp.customer_id

GROUP BY cs.segment

ORDER BY revenue_at_risk DESC;


-- ============================================================
-- 8. SEGMENT PERFORMANCE MATRIX
-- ============================================================

SELECT

    cs.segment,

    COUNT(*) AS customers,

    ROUND(
        AVG(cf.recency),
        2
    ) AS avg_recency,

    ROUND(
        AVG(cf.frequency),
        2
    ) AS avg_frequency,

    ROUND(
        AVG(cf.monetary),
        2
    ) AS avg_monetary,

    ROUND(
        AVG(cf.average_order_value),
        2
    ) AS avg_order_value,

    ROUND(
        AVG(cp.churn_probability),
        4
    ) AS avg_churn_probability

FROM customer_segments cs

JOIN customer_features cf

    ON cs.customer_id = cf.customer_id

LEFT JOIN churn_predictions cp

    ON cs.customer_id = cp.customer_id

GROUP BY cs.segment

ORDER BY avg_monetary DESC;


-- ============================================================
-- 9. CHAMPIONS
-- ============================================================

SELECT

    cs.customer_id,

    cf.recency,

    cf.frequency,

    cf.monetary,

    cs.rfm_score,

    cs.segment

FROM customer_segments cs

JOIN customer_features cf

    ON cs.customer_id = cf.customer_id

WHERE

    cf.recency <= 30

    AND cf.frequency >= 10

    AND cf.monetary >= 1000

ORDER BY cf.monetary DESC;


-- ============================================================
-- 10. AT-RISK CUSTOMERS BY SEGMENT
-- ============================================================

SELECT

    cs.segment,

    cs.customer_id,

    cf.recency,

    cf.frequency,

    cf.monetary,

    cp.churn_probability

FROM customer_segments cs

JOIN customer_features cf

    ON cs.customer_id = cf.customer_id

LEFT JOIN churn_predictions cp

    ON cs.customer_id = cp.customer_id

WHERE

    cf.recency > 90

    AND cf.monetary > 500

ORDER BY

    cp.churn_probability DESC NULLS LAST,

    cf.monetary DESC;


-- ============================================================
-- 11. SEGMENT REVENUE RANK
-- ============================================================

SELECT

    segment,

    SUM(
        cf.monetary
    ) AS revenue,

    RANK() OVER (

        ORDER BY
        SUM(cf.monetary) DESC

    ) AS revenue_rank

FROM customer_segments cs

JOIN customer_features cf

    ON cs.customer_id = cf.customer_id

GROUP BY segment;


-- ============================================================
-- 12. SEGMENT CUSTOMER VALUE
-- ============================================================

SELECT

    cs.segment,

    COUNT(*) AS customers,

    SUM(cf.monetary) AS total_revenue,

    ROUND(

        SUM(cf.monetary)
        /
        NULLIF(COUNT(*), 0),

        2

    ) AS revenue_per_customer

FROM customer_segments cs

JOIN customer_features cf

    ON cs.customer_id = cf.customer_id

GROUP BY cs.segment

ORDER BY revenue_per_customer DESC;