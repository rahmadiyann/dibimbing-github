{{ config(materialized='table') }}


WITH t_data AS (
    SELECT DISTINCT 
        `Fulfilment` AS fulfilment, 
        COALESCE(`fulfilled-by`, '-') AS fullfiled_by
    FROM `spotify-streaming-de-project.dbt_learning.amazon_sale_report`
)

SELECT
    {{ dbt_utils.generate_surrogate_key([
        'fulfilment',
        'fullfiled_by'
    ])}} AS fulfilment_id,*
FROM t_data