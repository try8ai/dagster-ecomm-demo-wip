{{ config(materialized='table') }}

--with orders_transformed as (
  select
    order_id,
    created_at::datetime + interval 1 day as created_at,
    currency_code,
    receipt_number,
    total_gross,
    total_tax,
    total_net,
    payment_method,
    paid_amount,
    customer_id
  from {{source('orders', 'orders')}}
--)

--select * from orders_transformed
