{{ config(materialized='view') }}

SELECT
    id,
    date,
    text,
    has_media,
    media_type,
    channel,
    media_path,
    LENGTH(text) AS text_length
FROM {{ source('raw', 'telegram_messages') }}
