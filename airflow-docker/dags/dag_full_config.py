from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
@dag(
    dag_id="dag_full_config",
    start_date=days_ago(1),
    schedule_interval="*/5 * * * *",
    catchup=False,
    tags=["dag_full_config"],
    params={"example_key": "example_value"},
    default_args={
        "owner": ["airflow", "rian"],
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "email_on_failure": False,
        "email_on_retry": False,
    },
    owner_links={
        "rian": "rian@gmail.com",
        "airflow": "airflow@gmail.com",
    },
)
def dag_full_config():
    start_task = EmptyOperator(task_id="start_task")
    end_task = EmptyOperator(task_id="end_task")

    start_task >> end_task
