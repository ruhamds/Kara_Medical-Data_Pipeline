select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select date
from "telegram_db"."public"."dim_dates"
where date is null



      
    ) dbt_internal_test