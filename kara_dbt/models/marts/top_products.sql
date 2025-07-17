-- models/marts/top_products.sql

SELECT
    LOWER(REGEXP_REPLACE(SPLIT_PART(message, CHR(10), 1), '[^a-zA-Z0-9 ]', '', 'g')) AS product_name,
    COUNT(*) AS mentions
FROM {{ ref('fct_messages') }}
WHERE message ILIKE '%price%' -- basic heuristic to catch product ads
GROUP BY 1
ORDER BY mentions DESC
