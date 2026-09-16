from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import sys
sys.path.append("/opt/airflow/include/youtube")

from youtube_api import extract_youtube_data



with DAG(
    dag_id = "youtube_extract",
    start_date = datetime(2026,9,16),
    schedule = None,
    catchup = False,
) as dag :
    
    extract = PythonOperator(
        task_id = "extract_youtube",
        python_callable = extract_youtube_data
    )