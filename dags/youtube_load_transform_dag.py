from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
sys.path.append("/opt/airflow/include/youtube")

from load_staging import load_to_staging
from transform_core import transform_to_core


with DAG(
    dag_id ="youtube_load_transform",
    start_date = datetime(2026,9,17),
    schedule = None,
    catchup = False

) as dag :

    load_staging_task = PythonOperator(
        task_id = "load_staging",
        python_callable = load_to_staging
    )

    transform_core_task =PythonOperator(
        task_id = "transform_core",
        python_callable = transform_to_core
    )

    load_staging_task >> transform_core_task


