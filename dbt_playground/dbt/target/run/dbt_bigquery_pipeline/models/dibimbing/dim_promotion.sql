
  
    

    create or replace table `spotify-streaming-de-project`.`dbt_learning`.`dim_promotion`
    
    

    OPTIONS()
    as (
      

WITH t_data AS (
    SELECT DISTINCT 
        `promotion-ids` AS promotion_ids
    FROM `spotify-streaming-de-project.dbt_learning.amazon_sale_report`
)

SELECT
    
    
to_hex(md5(cast(coalesce(cast(promotion_ids as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS promotion_id,*
FROM t_data
    );
  