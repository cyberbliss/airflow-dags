"""
Example Airflow DAG for an SGSS pipeline
"""

import os, datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.dates import days_ago
#from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2019,1,1),
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=2),
}
dag = DAG(
    'sgss_demo_pipeline_v_0_1_0',
    default_args=default_args,
    description='A DAG to demo an SGSS pipeline',
    schedule_interval=None,
)

with dag:
    step1 = KubernetesPodOperator(
        task_id="step1",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"hello world\")'"],
        name="sgss-demo-pipeline-step1",
        dag=dag,
    )

    step1