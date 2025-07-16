{{ config(materialized='view') }}

SELECT
    object_label,
    COUNT(*) AS count
FROM {{ ref('stg_detected_objects') }}
GROUP BY object_label
ORDER BY count DESC
LIMIT 10
