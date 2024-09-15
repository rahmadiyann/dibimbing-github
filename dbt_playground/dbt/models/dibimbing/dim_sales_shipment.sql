{{ config(materialized='table') }}

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
    {{ dbt_utils.generate_surrogate_key([
        'courier_status',
        'ship_city',
        'ship_state',
        'ship_postal_code',
    ])}} AS sales_shipment_id, *
FROM t_data