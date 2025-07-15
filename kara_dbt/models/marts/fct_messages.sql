SELECT DISTINCT
    m.message_id,
    m.message_date,
    m.message,
    m.has_media,
    m.media_type,
    m.media_url,
    m.message_length,
    c.channel_id,
    d.date AS date_id
FROM {{ ref('stg_telegram_messages') }} m
JOIN {{ ref('dim_channels') }} c ON m.channel = c.channel_name
JOIN {{ ref('dim_dates') }} d ON date_trunc('day', m.message_date) = d.date
WHERE m.message_id IS NOT NULL

