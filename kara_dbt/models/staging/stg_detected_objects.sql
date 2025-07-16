{{ config(materialized='view') }}

SELECT
    message_id,
    object_label,
    confidence,
    bounding_box,
    media_path
FROM {{ source('raw', 'detected_objects') }}
