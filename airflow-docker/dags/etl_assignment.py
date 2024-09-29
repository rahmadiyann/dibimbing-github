from airflow.decorators import task, dag
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.models.param import Param
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import requests
from flatten_dict import flatten

import os

@dag(
    dag_id='etl_assignment',
    description='ETL assignment. Fetch data from API based on table name, flatten the json and load it into sqlite and file based on output type and extension type. Default: users table, csv extension, sqlite output',
    schedule_interval="@daily",
    start_date=datetime(2024, 9, 29),
    catchup=False,
    params={
        "table": Param("users", enum=["users", "recipes", "products"]),
        "extension": Param("csv", enum=["csv", "parquet", "json"]),
        "output": Param("sqlite", enum=["sqlite", "file"])
    }
)

def etl_process():
    
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end', trigger_rule=TriggerRule.ONE_SUCCESS)
    wait_extract = EmptyOperator(task_id='wait_extract', trigger_rule=TriggerRule.ONE_SUCCESS)
    wait_load = EmptyOperator(task_id='wait_load', trigger_rule=TriggerRule.ONE_SUCCESS)
    
    def cleanup():
        os.system("rm -rf dags/data/staging/*")
        print("Staging folder cleaned up")
    
    cleanup = PythonOperator(
        task_id='cleanup',
        python_callable=cleanup
    )
    
    def precheck(**context):
        table = context['params']['table']
        print(f"Table: {table}")
        extension = context['params']['extension']
        print(f"Extension: {extension}")
        output = context['params']['output']
        print(f"Output: {output}")
        if table not in ['users', 'recipes', 'products']:
            raise ValueError(f"Unsupported table: {table}")
        if extension not in ['csv', 'parquet', 'json']:
            raise ValueError(f"Unsupported extension: {extension}")
        if output not in ['sqlite', 'file']:
            raise ValueError(f"Unsupported output type: {output}")

        # create folders
        os.makedirs(f"dags/data/staging/", exist_ok=True)
        os.makedirs(f"dags/data/output/", exist_ok=True)
        os.makedirs(f"dags/data/db_output/", exist_ok=True)
        
        print("Folders created successfully")
        
    precheck = PythonOperator(
        task_id='precheck',
        python_callable=precheck
    )
    
    def choose_extension(**context):
        extension = context['params']['extension']
        if extension == 'csv':
            return 'source_to_csv'
        elif extension == 'json':
            return 'source_to_json'
        elif extension == 'parquet':
            return 'source_to_parquet'
        else:
            raise ValueError(f"Unsupported extension: {extension}")

    branch_extension = BranchPythonOperator(
        task_id='branch_extension',
        python_callable=choose_extension
    )
    
    def choose_output(**context):
        output = context['params']['output']
        if output == 'sqlite':
            return 'load_to_sqlite'
        elif output == 'file':
            return 'load_to_file'
        else:
            raise ValueError(f"Unsupported output type: {output}")
        
    branch_output = BranchPythonOperator(
        task_id='branch_output',
        python_callable=choose_output
    )
    
    @task
    def source_to_csv(**context):
        table = context['params']['table']
        url = f"https://dummyjson.com/{table}"
        response = requests.get(url).json()
        data = []
        for i in response[table]:
            do_flatten = flatten(i, reducer='dot')
            flat_data = {k: str(v) for k, v in do_flatten.items()}
            data.append(flat_data)
        df = pd.DataFrame(data)
        df.to_csv(f"dags/data/staging/{table}.csv", index=False)
        
    @task
    def source_to_json(**context):
        table = context['params']['table']
        url = f"https://dummyjson.com/{table}"
        response = requests.get(url).json()
        data = []
        for i in response[table]:
            do_flatten = flatten(i, reducer='dot')
            flat_data = {k: str(v) for k, v in do_flatten.items()}
            data.append(flat_data)
        df = pd.DataFrame(data)
        df.to_json(f"dags/data/staging/{table}.json", orient='records', lines=True, index=False)
        
    @task
    def source_to_parquet(**context):
        table = context['params']['table']
        url = f"https://dummyjson.com/{table}"
        response = requests.get(url).json()
        data = []
        for i in response[table]:
            do_flatten = flatten(i, reducer='dot')
            flat_data = {k: str(v) for k, v in do_flatten.items()}
            data.append(flat_data)
        df = pd.DataFrame(data)
        df.to_parquet(f"dags/data/staging/{table}.parquet", index=False)

    source_to_csv_task = source_to_csv()
    source_to_json_task = source_to_json()
    source_to_parquet_task = source_to_parquet()

    @task
    def load_to_file(**context):
        table = context['params']['table']
        extension = context['params']['extension']
        if extension == 'csv':
            df = pd.read_csv(f"dags/data/staging/{table}.csv")
            df.to_csv(f"dags/data/output/{table}.csv", index=False)
        elif extension == 'json':
            df = pd.read_json(f"dags/data/staging/{table}.json", orient='records', lines=True)
            df.to_json(f"dags/data/output/{table}.json", orient='records', lines=True, index=False)
        elif extension == 'parquet':
            df = pd.read_parquet(f"dags/data/staging/{table}.parquet")
            df.to_parquet(f"dags/data/output/{table}.parquet", index=False)
            
        print(f"Data from {table} table has been saved to {extension} file.")
        print(f"Data: {df.head()}")
        
    load_to_file_task = load_to_file()

    @task
    def load_to_sqlite(**context):
        table = context['params']['table']
        extension = context['params']['extension']
        engine = create_engine(f'sqlite:///dags/data/db_output/{table}.db')
        if extension == 'csv':
            df = pd.read_csv(f"dags/data/staging/{table}.csv")
        elif extension == 'json':
            df = pd.read_json(f"dags/data/staging/{table}.json", orient='records', lines=True)
        elif extension == 'parquet':
            df = pd.read_parquet(f"dags/data/staging/{table}.parquet")
        else:
            raise ValueError(f"Unsupported extension: {extension}")
        
        # Check if the database file exists
        if os.path.exists(f"dags/data/db_output/{table}.db"):
            df.to_sql(table, engine, if_exists='replace', index=False)
        else:
            df.to_sql(table, engine, if_exists='append', index=False)
        print(f"Data: {pd.read_sql(f'SELECT * FROM {table}', engine).head()}")

    load_to_sqlite_task = load_to_sqlite()

    start >> precheck >> branch_extension
    branch_extension >> [source_to_csv_task, source_to_json_task, source_to_parquet_task] >> wait_extract
    wait_extract >> branch_output
    branch_output >> [load_to_file_task, load_to_sqlite_task] >> wait_load
    wait_load >> cleanup >> end

etl_process()