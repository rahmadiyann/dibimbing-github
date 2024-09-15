
  
    

    create or replace table `spotify-streaming-de-project`.`dbt_learning`.`dim_product`
    
    

    OPTIONS()
    as (
      

WITH t_data AS (
    SELECT DISTINCT 
        `Style` AS style,
        'SKU' AS sku,
        'Category' AS category,
        'Size' AS size
    FROM `spotify-streaming-de-project.dbt_learning.amazon_sale_report`
)

SELECT
    
    
to_hex(md5(cast(coalesce(cast(SKU as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS product_id,*
FROM t_data
    );
  