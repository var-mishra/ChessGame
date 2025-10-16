from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import os

CLICKHOUSE_URL = os.getenv("CLICKHOUSE_HTTP_URL", "http://clickhouse:8123")
DB = os.getenv("CLICKHOUSE_DB", "cdc")
TABLE = os.getenv("CLICKHOUSE_TABLE", "debezium_raw")


def run_aggregation():
    # Example: count customers ingested per day
    query = f"""
    SELECT toDate(event_time) as day, count() as events
    FROM {DB}.{TABLE}
    GROUP BY day
    ORDER BY day
    FORMAT CSVWithNames
    """
    resp = requests.post(f"{CLICKHOUSE_URL}/?query=", data=query)
    resp.raise_for_status()
    csv_text = resp.text
    print(csv_text)
    with open('/opt/airflow/logs/nightly_aggregation.csv', 'w') as f:
        f.write(csv_text)


def default_args():
    return {
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 0,
        'retry_delay': timedelta(minutes=5),
    }

with DAG(
    dag_id='nightly_clickhouse_aggregation',
    default_args=default_args(),
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=20),
    tags=['analytics', 'clickhouse']
) as dag:

    aggregate = PythonOperator(
        task_id='aggregate_clickhouse',
        python_callable=run_aggregation,
    )
