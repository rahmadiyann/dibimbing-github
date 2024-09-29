from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from datetime import datetime

@dag(
    dag_id="decorator_dag",
    start_date=datetime.now(),
    schedule_interval="@daily",
    catchup=False,
)
def decorator_dag():
    start_task = EmptyOperator(task_id="start_task")
    end_task = EmptyOperator(task_id="end_task")

    start_task >> end_task

decorator_dag()