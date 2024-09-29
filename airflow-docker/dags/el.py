from airflow import DAG
from airflow.decorators import task, dag
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models.param import Param
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
import pandas as pd
import json
from sqlalchemy import create_engine

@dag(
    dag_id='etl_process',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    params={
        "source_type": Param("csv", enum=["csv", "json", "parquet"]),
        "extract_data": Param("users_data", description="Name of the file to extract (without extension)")
    }
)
def etl_process():

    def choose_extract_task(**context):
        source_type = context['params']['source_type']
        if source_type == 'csv':
            return 'extract_csv'
        elif source_type == 'json':
            return 'extract_json'
        elif source_type == 'parquet':
            return 'extract_parquet'
        else:
            raise ValueError(f"Unsupported source type: {source_type}")

    branch_task = BranchPythonOperator(
        task_id='branch_task',
        python_callable=choose_extract_task
    )

    @task(task_id='extract_csv')
    def extract_csv(**context):
        filename = context['params']['extract_data']
        df = pd.read_csv(f"data/{filename}.csv")
        df.to_csv(f"data/staging_{filename}.csv", index=False)
        return f"data/staging_{filename}.csv"

    @task(task_id='extract_json')
    def extract_json(**context):
        filename = context['params']['extract_data']
        with open(f"data/{filename}.json", 'r') as file:
            data = json.load(file)
        df = pd.DataFrame(data)
        df.to_csv(f"data/staging_{filename}.csv", index=False)
        return f"data/staging_{filename}.csv"

    @task(task_id='extract_parquet')
    def extract_parquet(**context):
        filename = context['params']['extract_data']
        df = pd.read_parquet(f"data/{filename}.parquet")
        df.to_csv(f"data/staging_{filename}.csv", index=False)
        return f"data/staging_{filename}.csv"

    @task(task_id='load_to_sqlite', trigger_rule=TriggerRule.ONE_SUCCESS)
    def load_to_sqlite(staging_file):
        engine = create_engine('sqlite:///data/etl_output.db')
        df = pd.read_csv(staging_file)
        table_name = staging_file.split('_')[-1].split('.')[0]
        df.to_sql(table_name, engine, if_exists='replace', index=False)

    extract_csv_task = extract_csv()
    extract_json_task = extract_json()
    extract_parquet_task = extract_parquet()
    end_task = EmptyOperator(task_id='end_task', trigger_rule=TriggerRule.ONE_SUCCESS)

    # Corrected task dependencies
    branch_task >> [extract_csv_task, extract_json_task, extract_parquet_task]
    load_to_sqlite(extract_csv_task)
    load_to_sqlite(extract_json_task)
    load_to_sqlite(extract_parquet_task)
    [extract_csv_task, extract_json_task, extract_parquet_task] >> end_task

dag = etl_process()