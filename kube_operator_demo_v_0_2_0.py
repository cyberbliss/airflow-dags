"""
Example Airflow DAG for Google Kubernetes Engine.
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
    'kube_operator_demo_v_0_2_0',
    default_args=default_args,
    description='A simple DAG to demo the Kube operator',
    schedule_interval=None,
)

with dag:
    pt1 = KubernetesPodOperator(
        task_id="pt1",
        in_cluster=True,
        namespace="airflow",
        image="bash",
        cmds=['echo'],
        arguments=['{{ ds }}'],
        name="pod-pt1",
        dag=dag,
    )

    pt2 = KubernetesPodOperator(
        task_id="pt2",
        in_cluster=True,
        namespace="airflow",
        image="python:3.7",
        cmds=['python','-c'],
        arguments=["print('hello world')"],
        name="pod-pt2",
        dag=dag,
    )

    pt1 >> pt2

