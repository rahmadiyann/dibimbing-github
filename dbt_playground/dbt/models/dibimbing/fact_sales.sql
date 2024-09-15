{{ config(materialized='table') }}

SELECT 
  index AS sales_id,
  `Order ID` as order_id,
  Date as date,
  Status as status,
  {{ dbt_utils.generate_surrogate_key([
        'Fulfilment',
        '`fulfilled-by`'
    ])}} AS fulfilment_id,
  {{ dbt_utils.generate_surrogate_key([
        'SKU'
    ])}} AS product_id,
  {{ dbt_utils.generate_surrogate_key([
        '`promotion-ids`'
    ])}} AS promotion_id,
  {{ dbt_utils.generate_surrogate_key([
        '`Sales Channel `'
    ])}} AS sales_channel_id,
  {{ dbt_utils.generate_surrogate_key([
        '`Courier Status`',
        '`ship-city`',
        '`ship-state`',
        '`ship-postal-code`',
    ])}} AS sales_shipment_id,
  Qty as qty,
  Amount as amount
FROM spotify-streaming-de-project.dbt_learning.amazon_sale_report 