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
    tags=['PHE'],
)

with dag:
    step1 = KubernetesPodOperator(
        task_id="step1-QUERY_SGSS",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** QUERY SGSS ****\")'"],
        name="sgss-demo-pipeline-step1",
        dag=dag,
    )

    step2 = KubernetesPodOperator(
        task_id="step2-PREPROCESSING",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** PRE-PROCESSING ****\")'"],
        name="sgss-demo-pipeline-step2",
        dag=dag,
    )    

    step3 = KubernetesPodOperator(
        task_id="step3-LAB_QUALITY_CONTROL",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** REMOVE LAB QUALITY CONTROL SAMPLES ****\")'"],
        name="sgss-demo-pipeline-step3",
        dag=dag,
    )    

    step4 = KubernetesPodOperator(
        task_id="step4-PATIENT_GROUPING",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** GROUP RECORDS AT PATIENT LEVEL ****\")'"],
        name="sgss-demo-pipeline-step4",
        dag=dag,
    )    

    step5A = KubernetesPodOperator(
        task_id="step5A-MONO_GROUPING",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** MONOMICROBIAL GROUPING ****\")'"],
        name="sgss-demo-pipeline-step5A",
        dag=dag,
    )    

    step5B = KubernetesPodOperator(
        task_id="step5B-POLY_GROUPING",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** POLYMICROBIAL GROUPING ****\")'"],
        name="sgss-demo-pipeline-step5B",
        dag=dag,
    )

    step6A = KubernetesPodOperator(
        task_id="step6A-ORGANISM_RECODING",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** ORGANISM RECODING ****\")'"],
        name="sgss-demo-pipeline-step6A",
        dag=dag,
    )

    step6B = KubernetesPodOperator(
        task_id="step6B-STREP_RECODING",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** STREP RECODING ****\")'"],
        name="sgss-demo-pipeline-step6B",
        dag=dag,
    )

    step6C = KubernetesPodOperator(
        task_id="step6B-STAPH_RECODING",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** STAPH RECODING ****\")'"],
        name="sgss-demo-pipeline-step6C",
        dag=dag,
    )    

    step7 = KubernetesPodOperator(
        task_id="step7-RESPECIATE",
        in_cluster=True,
        namespace="airflow",
        image="eu.gcr.io/service-project-gke-c830/mc-demo:latest",
        cmds=['bash','-c'],
        arguments=["Rscript -e 'print(\"**** RESPECIATE ****\")'"],
        name="sgss-demo-pipeline-step7",
        dag=dag,
    ) 

    step1 >> step2 >> step3 >> step4 >> step5A >> step5B >> [step6A, step6B, step6C] >> step7