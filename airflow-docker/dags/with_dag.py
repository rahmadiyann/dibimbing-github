from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id="with_dag",
    start_date=datetime.now(),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    start_task = EmptyOperator(task_id="start_task")
    end_task = EmptyOperator(task_id="end_task")
    
    start_task >> end_task