{{ config(materialized='table') }}

SELECT DISTINCT
    date_trunc('day', date) AS date,
    EXTRACT(YEAR FROM date_trunc('day', date)) AS year,
    EXTRACT(MONTH FROM date_trunc('day', date)) AS month,
    EXTRACT(DAY FROM date_trunc('day', date)) AS day,
    EXTRACT(DOW FROM date_trunc('day', date)) AS day_of_week
FROM {{ ref('stg_telegram_messages') }}