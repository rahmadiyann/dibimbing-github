
  
    

    create or replace table `spotify-streaming-de-project`.`dbt_learning`.`dim_sales_channel`
    
    

    OPTIONS()
    as (
      

WITH t_data AS (
    SELECT DISTINCT 
        `Sales Channel ` AS sales_channel,
    FROM `spotify-streaming-de-project.dbt_learning.amazon_sale_report`
)

SELECT
    
    
to_hex(md5(cast(coalesce(cast(sales_channel as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS sales_channel_id,*
FROM t_data
    );
  