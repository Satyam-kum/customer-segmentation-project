-- ============================================================
-- RETENTION ANALYSIS
-- ============================================================


-- ============================================================
-- 1. HIGH-RISK CUSTOMERS
-- ============================================================

SELECT

    cp.customer_id,

    cp.churn_probability,

    cp.churn_risk,

    cp.retention_action,

    cp.monetary,

    cp.frequency,

    cp.recency,

    cs.segment

FROM churn_predictions cp

LEFT JOIN customer_segments cs

    ON cp.customer_id = cs.customer_id

WHERE cp.churn_risk = 'HIGH'

ORDER BY

    cp.churn_probability DESC;


-- ============================================================
-- 2. HIGH-VALUE HIGH-RISK CUSTOMERS
-- ============================================================

SELECT

    cp.customer_id,

    cp.churn_probability,

    cp.monetary,

    cp.frequency,

    cp.recency,

    cp.retention_action,

    cs.segment

FROM churn_predictions cp

LEFT JOIN customer_segments cs

    ON cp.customer_id = cs.customer_id

WHERE cp.churn_probability >= 0.75

  AND cp.monetary >= 1000

ORDER BY

    cp.monetary DESC;


-- ============================================================
-- 3. REVENUE AT RISK
-- ============================================================

SELECT

    SUM(monetary)
        AS revenue_at_risk,

    COUNT(*)
        AS high_risk_customers

FROM churn_predictions

WHERE churn_risk = 'HIGH';


-- ============================================================
-- 4. REVENUE AT RISK BY SEGMENT
-- ============================================================

SELECT

    cs.segment,

    COUNT(
        cp.customer_id
    ) AS customers,

    SUM(
        cp.monetary
    ) AS revenue_at_risk,

    AVG(
        cp.churn_probability
    ) AS average_churn_probability

FROM churn_predictions cp

LEFT JOIN customer_segments cs

    ON cp.customer_id = cs.customer_id

WHERE cp.churn_risk = 'HIGH'

GROUP BY cs.segment

ORDER BY revenue_at_risk DESC;


-- ============================================================
-- 5. CHURN RISK DISTRIBUTION
-- ============================================================

SELECT

    churn_risk,

    COUNT(*) AS customers,

    SUM(monetary) AS customer_value,

    AVG(churn_probability)
        AS average_probability

FROM churn_predictions

GROUP BY churn_risk

ORDER BY

    CASE churn_risk

        WHEN 'HIGH' THEN 1

        WHEN 'MEDIUM' THEN 2

        WHEN 'LOW' THEN 3

        ELSE 4

    END;


-- ============================================================
-- 6. RETENTION ACTION DISTRIBUTION
-- ============================================================

SELECT

    retention_action,

    COUNT(*) AS customers,

    SUM(monetary)
        AS customer_value,

    AVG(churn_probability)
        AS average_churn_probability

FROM churn_predictions

GROUP BY retention_action

ORDER BY customers DESC;


-- ============================================================
-- 7. PRIORITIZED RETENTION CAMPAIGN
-- ============================================================

SELECT

    cp.customer_id,

    cp.churn_probability,

    cp.monetary,

    cp.frequency,

    cp.recency,

    cp.churn_risk,

    cp.retention_action,

    CASE

        WHEN cp.churn_probability >= 0.75
             AND cp.monetary >= 5000

            THEN 'CRITICAL'

        WHEN cp.churn_probability >= 0.75
             AND cp.monetary >= 1000

            THEN 'VERY HIGH'

        WHEN cp.churn_probability >= 0.75

            THEN 'HIGH'

        WHEN cp.churn_probability >= 0.45

            THEN 'MEDIUM'

        ELSE

            'LOW'

    END AS priority

FROM churn_predictions cp

ORDER BY

    cp.churn_probability DESC,

    cp.monetary DESC;


-- ============================================================
-- 8. VIP CUSTOMERS AT RISK
-- ============================================================

SELECT

    cp.customer_id,

    cp.monetary,

    cp.frequency,

    cp.recency,

    cp.churn_probability,

    cp.retention_action

FROM churn_predictions cp

WHERE cp.monetary >= 1000

  AND cp.churn_probability >= 0.75

ORDER BY

    cp.monetary DESC;


-- ============================================================
-- 9. CUSTOMERS WHO ARE BECOMING INACTIVE
-- ============================================================

SELECT

    customer_id,

    recency,

    frequency,

    monetary,

    CASE

        WHEN recency > 180
            THEN 'INACTIVE'

        WHEN recency > 90
            THEN 'AT RISK'

        WHEN recency > 60
            THEN 'WARNING'

        ELSE
            'ACTIVE'

    END AS activity_status

FROM customer_features

ORDER BY recency DESC;


-- ============================================================
-- 10. CUSTOMER REACTIVATION TARGETS
-- ============================================================

SELECT

    customer_id,

    recency,

    frequency,

    monetary,

    average_order_value

FROM customer_features

WHERE recency BETWEEN 90 AND 365

  AND frequency >= 2

ORDER BY monetary DESC;


-- ============================================================
-- 11. RETENTION OPPORTUNITY SCORE
-- ============================================================

SELECT

    cp.customer_id,

    cp.churn_probability,

    cp.monetary,

    ROUND(

        cp.churn_probability
        * cp.monetary,

        2

    ) AS retention_opportunity_value,

    cp.retention_action

FROM churn_predictions cp

ORDER BY

    retention_opportunity_value DESC;


-- ============================================================
-- 12. EXPECTED REVENUE LOSS
-- ============================================================

SELECT

    SUM(

        churn_probability
        * monetary

    ) AS expected_revenue_loss

FROM churn_predictions;


-- ============================================================
-- 13. EXPECTED REVENUE LOSS BY RISK
-- ============================================================

SELECT

    churn_risk,

    COUNT(*) AS customers,

    SUM(

        churn_probability
        * monetary

    ) AS expected_revenue_loss

FROM churn_predictions

GROUP BY churn_risk

ORDER BY expected_revenue_loss DESC;


-- ============================================================
-- 14. RETENTION CAMPAIGN SUMMARY
-- ============================================================

SELECT

    retention_action,

    COUNT(*) AS customers,

    SUM(monetary) AS revenue_exposed,

    SUM(

        churn_probability
        * monetary

    ) AS expected_revenue_loss

FROM churn_predictions

GROUP BY retention_action

ORDER BY expected_revenue_loss DESC;