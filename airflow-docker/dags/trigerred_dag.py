from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import time
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 5),
    'catchup': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'trigerred_dag_testing',
    default_args=default_args,
    description='A simple DAG with start > process > end tasks',
    schedule_interval=timedelta(days=1),
)

def start_task():
    print("DAG Triggered")

def process_task():
    time.sleep(10)

def end_task():
    print("Ending the DAG")

start = PythonOperator(
    task_id='start',
    python_callable=start_task,
    dag=dag,
)

process = PythonOperator(
    task_id='process',
    python_callable=process_task,
    dag=dag,
)

end = PythonOperator(
    task_id='end',
    python_callable=end_task,
    dag=dag,
)

start >> process >> end
