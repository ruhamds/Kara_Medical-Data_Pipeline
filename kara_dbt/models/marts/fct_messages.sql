{{ config(materialized='table') }}

SELECT
    m.id,
    m.date,
    m.text,
    m.has_media,
    m.media_type,
    m.media_path,
    m.text_length,
    c.channel_id,
    d.date AS date_id
FROM {{ ref('stg_telegram_messages') }} m
JOIN {{ ref('dim_channels') }} c ON m.channel = c.channel_name
JOIN {{ ref('dim_dates') }} d ON date_trunc('day', m.date) = d.date
WHERE m.id IS NOT NULL