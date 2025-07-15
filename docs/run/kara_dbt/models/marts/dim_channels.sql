
  create view "telegram_db"."public"."dim_channels__dbt_tmp"
    
    
  as (
    SELECT DISTINCT
    channel AS channel_name,
    DENSE_RANK() OVER (ORDER BY channel) AS channel_id
FROM "telegram_db"."public"."stg_telegram_messages"
  );