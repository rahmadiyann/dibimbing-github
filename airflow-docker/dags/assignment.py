from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import yaml

# Daftar tabel yang akan diekstrak
with open("dags/resources/assignment/tables.yaml") as f:
    MYSQL_TABLES = yaml.safe_load(f)

# Konfigurasi DAG
default_args = {
    'owner': 'rian',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'el_assignment',
    default_args=default_args,
    description='Extract data dari MySQL ke PostgreSQL. DAG assignment kelas ETL with Airflow Day 15 Data Engineering Batch 7 di Dibimbing.id',
    schedule_interval='15 9-21/2 1-7,15-21 * 5', 
    catchup=False
)

start = EmptyOperator(task_id="start")
end = EmptyOperator(task_id="end")
wait = EmptyOperator(task_id="wait")

def create_directory() -> None:
    """Membuat direktori untuk staging data"""
    import os
    os.makedirs('resources/assignment/staging', exist_ok=True)
    print('Directory created')

fs_precheck = PythonOperator(
    task_id='fs_precheck',
    python_callable=create_directory,
    dag=dag
)

mysql_precheck = SQLExecuteQueryOperator(
    task_id = "mysql_precheck",
    conn_id = "mysql_dibimbing",
    sql     = f"resources/assignment/mysql_precheck.sql",
    dag     = dag
)

psql_precheck = SQLExecuteQueryOperator(
    task_id = "psql_precheck",
    conn_id = "postgres_dibimbing",
    sql     = f"resources/assignment/psql_precheck.sql",
    dag     = dag
)

cleanup = BashOperator(
    task_id = "cleanup",
    bash_command = "rm -rf resources/assignment/staging/*",
    dag = dag
)

def extract_data(table_name: str, **kwargs) -> None:
    """Mengambil data dari MySQL

    :param table_name: Nama table yang akan diambil
    """
    import pandas as pd
    # Extract data from MySQL
    mysql_hook = MySqlHook(mysql_conn_id='mysql_dibimbing')
    query = f"SELECT * FROM {table_name}"
    df = mysql_hook.get_pandas_df(query)
    
    # Write to CSV file
    csv_path = f"resources/assignment/staging/{table_name}.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"Extracted {len(df)} rows from {table_name} and saved to {csv_path}")

def load_data(table_name: str, **kwargs) -> None:
    """Memuat data ke PostgreSQL

    :param table_name: Nama table yang akan dimuat
    """
    import pandas as pd
    from sqlalchemy import create_engine
    
    # Read from CSV file
    csv_path = f"resources/assignment/staging/{table_name}.csv"
    df = pd.read_csv(csv_path)
    
    # Load data to PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='postgres_dibimbing')
    conn_uri = postgres_hook.get_uri()
    engine = create_engine(conn_uri)
    
    # Use SQLAlchemy to create the table and load data
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    print(f"Loaded {len(df)} rows to {table_name} in PostgreSQL")

def show_data(table_name: str, **kwargs) -> None:
    """Menampilkan data dari PostgreSQL

    :param table_name: Nama table yang akan ditampilkan
    """
    import pandas as pd
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    postgres_hook = PostgresHook("postgres_dibimbing").get_sqlalchemy_engine()

    with postgres_hook.connect() as conn:
        df = pd.read_sql(
            sql = f"SELECT * FROM {table_name}",
            con = conn,
        )

    print(df)
    


for table in MYSQL_TABLES:
    extract_task = PythonOperator(
        task_id=f'extract_{table}',
        python_callable=extract_data,
        op_kwargs={'table_name': table},
        dag=dag,
    )
    load_task = PythonOperator(
        task_id=f'load_{table}',
        python_callable=load_data,
        op_kwargs={'table_name': table},
        dag=dag,
    )
    
    query_postgres = PythonOperator(
        task_id=f'show_{table}',
        python_callable=show_data,
        op_kwargs={'table_name': table},
        dag=dag,
    )

    start >> fs_precheck >> [mysql_precheck, psql_precheck] >> wait >> extract_task >> load_task >> cleanup >> query_postgres >> end