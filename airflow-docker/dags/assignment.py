from airflow import DAG
from airflow.operators.python import PythonOperator  # Updated import
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook  # Updated import
from datetime import datetime, timedelta
import pandas as pd

# Daftar tabel yang akan diekstrak
MYSQL_TABLES = [
    'customers', 'orders', 'products', 'employees', 'suppliers', 'categories'
]

# Konfigurasi DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mysql_to_postgres_etl',
    default_args=default_args,
    description='Extract data from MySQL to PostgreSQL',
    schedule_interval='15 9-21/2 1-7,15-21 * 5',  # Cron expression as requested
    catchup=False
)

def extract_load_data(table_name, **kwargs):
    # Ekstrak data dari MySQL
    mysql_hook = MySqlHook(mysql_conn_id='mysql_conn')
    query = f"SELECT * FROM {table_name}"
    df = mysql_hook.get_pandas_df(query)
    
    # Load data ke PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn')
    postgres_hook.insert_rows(
        table=table_name,
        rows=df.values.tolist(),
        target_fields=df.columns.tolist(),
        replace=True
    )
    
    print(f"Extracted and loaded {len(df)} rows from {table_name}")

# Buat task untuk setiap tabel
for table in MYSQL_TABLES:
    task = PythonOperator(
        task_id=f'extract_load_{table}',
        python_callable=extract_load_data,
        op_kwargs={'table_name': table},
        dag=dag,
    )

# Anda bisa menambahkan dependensi antar task di sini jika diperlukan
# Misalnya: task_table1 >> task_table2 >> task_table3
