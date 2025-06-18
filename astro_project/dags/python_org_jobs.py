from include.Extraction import Extraction
from include.Transform import Transformation
from include.Load import Loading
import datetime
import os

from airflow import DAG
from airflow.operators.python import PythonOperator


with DAG(
    dag_id = "python_org_jobs",
    description = "ETL from python.org/jobs",
    tags = ["ETL", "Web Scraping", "bs4"],
    start_date = datetime.datetime(2025, 1, 1),
    schedule_interval = "@daily",
    catchup = False
) as dag:
    
    task_1 = PythonOperator(
        task_id = "Extract",
        python_callable = Extraction
    )

    task_2 = PythonOperator(
        task_id = "Transform",
        python_callable = Transformation
    )

    task_3 = PythonOperator(
        task_id = "Load",
        python_callable = Loading
    )

    task_1 >> task_2 >> task_3