import pandas as pd
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import get_current_context
from datetime import datetime, timedelta
import pendulum

pd.options.display.max_columns       = None
pd.options.display.expand_frame_repr = None

local_tz = pendulum.timezone("Asia/Jakarta")

@dag(
    dag_id="curr_context",
    start_date=datetime(2024, 1, 1, tzinfo=local_tz),
    schedule_interval="@daily",
    catchup=False
)
def current_context_with_function():
    start_task = EmptyOperator(task_id="start_task")
    end_task   = EmptyOperator(task_id="end_task")

    @task
    def print_all_context():
        context = get_current_context()
        df      = pd.DataFrame([
            {
                "key"  : key,
                "type" : str(type(value)),
                "value": str(value)
            }
            for key, value in context.items()]
        )

        print(f"\n{df}")
    @task
    def print_sample_context():
        context = get_current_context()

        print("=== logical date ==>")
        print("data interval start:", context['data_interval_start'])
        print("data interval end:", context['data_interval_end'])

        print("=== get date and timestamp ==>")
        print("ds:", context['ds'])
        print("ts:", context['ts'])

        print("=== task instance ==>")
        print("task instance execution_date:", context['ti'].start_date)
        print("task instance current_state:", context['ti'].current_state())

        print("=== realtime ==>")
        print("dag_run start_date:", context['dag_run'].start_date)
        print("dag_run start_task start_date:", context['dag_run'].get_task_instance('start_task').start_date)

        print("=== transform ==>")
        print("data interval end - wib:", context['data_interval_end'].in_timezone('Asia/Jakarta').add(days=-1).to_datetime_string())
        print("datetime - string:", datetime.strptime('2024-01-01 00:00:00', '%Y-%m-%d %H:%M:%S') - timedelta(days=1))

    start_task >> print_all_context() >> print_sample_context() >> end_task

current_context_with_function()