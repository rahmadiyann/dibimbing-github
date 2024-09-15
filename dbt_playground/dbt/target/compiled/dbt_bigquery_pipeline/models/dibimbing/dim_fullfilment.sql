


WITH t_data AS (
    SELECT DISTINCT 
        `Fulfilment` AS fulfilment, 
        COALESCE(`fulfilled-by`, '-') AS fullfiled_by
    FROM `spotify-streaming-de-project.dbt_learning.amazon_sale_report`
)

SELECT
    
    
to_hex(md5(cast(coalesce(cast(fulfilment as STRING), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(fullfiled_by as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS fulfilment_id,*
FROM t_data