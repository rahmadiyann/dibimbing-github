from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor

@dag()
def sensor_file():
    start_task = EmptyOperator(task_id="start_task")
    end_task   = EmptyOperator(task_id="end_task")

    wait_file = FileSensor(
        fs_conn_id    = "default_fs",
        task_id       = "wait_file",
        filepath      = "watch/text.txt",
        poke_interval = 5,
    )
   
    start_task >> wait_file >> end_task

sensor_file()