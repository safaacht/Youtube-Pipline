from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

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

    trigger_load_transform = TriggerDagRunOperator(
        task_id = "trigger_load_transform",
        trigger_dag_id = "youtube_load_transform"
    )

    extract >> trigger_load_transform