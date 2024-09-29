from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

dag = DAG(
    dag_id="complex_control_flow",
    start_date=datetime.now(),
    schedule_interval="@daily",
    catchup=False,
)

task_1 = EmptyOperator(task_id="task_1", dag=dag)
task_2 = EmptyOperator(task_id="task_2", dag=dag)
task_3 = EmptyOperator(task_id="task_3", dag=dag)
task_4 = EmptyOperator(task_id="task_4", dag=dag)
task_5 = EmptyOperator(task_id="task_5", dag=dag)
task_6 = EmptyOperator(task_id="task_6", dag=dag)
task_7 = EmptyOperator(task_id="task_7", dag=dag)
task_8 = EmptyOperator(task_id="task_8", dag=dag)
task_9 = EmptyOperator(task_id="task_9", dag=dag)
task_10 = EmptyOperator(task_id="task_10", dag=dag)

task_1 >> [task_2, task_3, task_4] >> task_6 >> [task_7, task_8]
task_5 >> [task_8, task_9] >> task_10