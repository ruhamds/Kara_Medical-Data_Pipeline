{{ config(materialized='view') }}

SELECT
    id AS message_id,
    date AS message_date,
    text AS message,
    has_media,
    media_type,
    channel,
    media_path AS media_url,
    LENGTH(text) AS message_length
FROM {{ source('raw', 'telegram_messages') }}
