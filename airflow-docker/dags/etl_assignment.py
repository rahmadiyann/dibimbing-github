from airflow.decorators import task, dag
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.models.param import Param
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import requests
from flatten_dict import flatten

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
    wait = EmptyOperator(task_id='wait', trigger_rule=TriggerRule.ONE_SUCCESS)
    
    def choose_extension(**context):
        extension = context['params']['extension']
        if extension == 'csv':
            return '2csv'
        elif extension == 'json':
            return '2json'
        elif extension == 'parquet':
            return '2parquet'
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
    def fetch_data(**context):
        table = context['params']['table']
        url = f"https://dummyjson.com/{table}"
        response = requests.get(url).json()
        do_flatten = flatten(response, reducer='dot')
        flat_data = {k: str(v) for k, v in do_flatten.items()}
        df = pd.DataFrame(flat_data)
        return df

    @task
    def load_to_file(df: pd.DataFrame, **context):
        extension = context['params']['extension']
        table = context['params']['table']
        if extension == 'csv':
            df.to_csv(f"data/{table}.csv", index=False)
        elif extension == 'json':
            df.to_json(f"data/{table}.json", orient='records', lines=True, index=False)
        elif extension == 'parquet':
            df.to_parquet(f"data/{table}.parquet", index=False)
        else:
            raise ValueError(f"Unsupported extension: {extension}")

    @task
    def load_to_sqlite(df: pd.DataFrame, **context):
        table = context['params']['table']
        engine = create_engine(f'sqlite:///data/db_output/{table}.db')
        df.to_sql(table, engine, if_exists='replace', index=False)
        print(pd.read_sql(f"SELECT * FROM {table}", engine))

    start >> fetch_data >> branch_extension
    branch_extension >> branch_output
    branch_output >> load_to_file >> wait
    branch_output >> load_to_sqlite >> wait
    wait >> end

etl_process()