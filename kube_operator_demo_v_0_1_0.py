"""
Example Airflow DAG for Google Kubernetes Engine.
"""

import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "example-project")
GCP_LOCATION = os.environ.get("GCP_GKE_LOCATION", "europe-north1-a")
CLUSTER_NAME = os.environ.get("GCP_GKE_CLUSTER_NAME", "cluster-name")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
dag = DAG(
    'kube_operator_demo_v_0_1_0',
    default_args=default_args,
    description='A simple DAG to demo the Kube operator',
    schedule_interval=None,
)

pt1 = KubernetesPodOperator(
    task_id="pod_task",
    in_cluster=True,
    namespace="airflow",
    image="bash",
    cmds=['echo'],
    arguments=['{{ ds }}'],
    name="test-pod",
    dag=dag,
)

pt1

