from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

@dag(
    dag_id="operators_dag",
    start_date=datetime.now(),
    schedule_interval="@daily",
    catchup=False,
)
def control_flow_parallel():
    start = EmptyOperator(task_id="start")
    task_2 = BashOperator(task_id="task_2", bash_command="echo 'Hello from bash'")
    task_3 = PythonOperator(task_id="task_3", python_callable=lambda: print("Hello from python"))
    end = EmptyOperator(task_id="end")
   
    start >> [task_2, task_3] >> end

control_flow_parallel()