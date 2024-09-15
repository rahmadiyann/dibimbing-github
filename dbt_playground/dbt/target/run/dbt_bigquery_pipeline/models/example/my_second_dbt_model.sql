

  create or replace view `spotify-streaming-de-project`.`dbt_learning`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `spotify-streaming-de-project`.`dbt_learning`.`my_first_dbt_model`
where id = 1;

