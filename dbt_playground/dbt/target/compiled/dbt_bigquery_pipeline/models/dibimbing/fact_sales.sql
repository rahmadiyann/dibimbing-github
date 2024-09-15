

SELECT 
  index AS sales_id,
  `Order ID` as order_id,
  Date as date,
  Status as status,
  
    
to_hex(md5(cast(coalesce(cast(Fulfilment as STRING), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(`fulfilled-by` as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS fulfilment_id,
  
    
to_hex(md5(cast(coalesce(cast(SKU as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS product_id,
  
    
to_hex(md5(cast(coalesce(cast(`promotion-ids` as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS promotion_id,
  
    
to_hex(md5(cast(coalesce(cast(`Sales Channel ` as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS sales_channel_id,
  
    
to_hex(md5(cast(coalesce(cast(`Courier Status` as STRING), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(`ship-city` as STRING), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(`ship-state` as STRING), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(`ship-postal-code` as STRING), '_dbt_utils_surrogate_key_null_') as STRING))) AS sales_shipment_id,
  Qty as qty,
  Amount as amount
FROM spotify-streaming-de-project.dbt_learning.amazon_sale_report