from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

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
    'trigger_dag',
    default_args=default_args,
    description='DAG to trigger trigerred_dag',
    schedule_interval=timedelta(days=1),
)

start = EmptyOperator(
    task_id='start',
    dag=dag,
)

end = EmptyOperator(
    task_id='end',
    dag=dag,
)

trigger_task = TriggerDagRunOperator(
    task_id='trigger_trigerred_dag',
    trigger_dag_id='trigerred_dag_testing',
    wait_for_completion=True,
    poke_interval=5,
    dag=dag,
)

start >> trigger_task >> end
