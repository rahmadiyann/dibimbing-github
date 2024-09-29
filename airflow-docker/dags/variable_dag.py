from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

dag = DAG(
    dag_id="variable_dag",
    start_date=datetime.now(),
    schedule_interval="@daily",
    catchup=False,
)

start_task = EmptyOperator(task_id="start_task", dag=dag)
end_task = EmptyOperator(task_id="end_task", dag=dag)

start_task >> end_task