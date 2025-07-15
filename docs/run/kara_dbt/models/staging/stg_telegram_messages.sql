
  create view "telegram_db"."public"."stg_telegram_messages__dbt_tmp"
    
    
  as (
    

SELECT
    id AS message_id,
    date AS message_date,
    text AS message,
    has_media,
    media_type,
    channel,
    media_path AS media_url,
    LENGTH(text) AS message_length
FROM "telegram_db"."raw"."telegram_messages"
  );