
  
    

    create or replace table `spotify-streaming-de-project`.`dbt_learning`.`dim_sales_shipment`
    
    

    OPTIONS()
    as (
      

WITH t_data AS (
    SELECT DISTINCT 
        '`Courier Status`' AS courier_status,
        `ship-service-level` as ship_service_level,
        `ship-city` as ship_city,
        `ship-state` as ship_state,
        `ship-postal-code` as ship_postal_code,
        `ship-country` as ship_country
    FROM `spotify-streaming-de-project.dbt_learning.amazon_sale_report`
)

SELECT
    
    
to_hex(md5(cast(coalesce(cast(courier_status as STRING), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ship_city as STRING), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ship_state as STRING), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ship_postal_code as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS sales_shipment_id, *
FROM t_data
    );
  