SELECT DISTINCT
    channel AS channel_name,
    DENSE_RANK() OVER (ORDER BY channel) AS channel_id
FROM {{ ref('stg_telegram_messages') }}
