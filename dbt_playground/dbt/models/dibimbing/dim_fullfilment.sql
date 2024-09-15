{{ config(materialized='table') }}

SELECT DISTINCT 
    `Fulfilment` AS fulfilment, 
    COALESCE(`fulfilled-by`, '-') AS fullfiled_by
FROM `spotify-streaming-de-project.dbt_learning.amazon_sale_report`