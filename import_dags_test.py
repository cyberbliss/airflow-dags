import pytest
from airflow.models import DagBag

def test_import_dags():
    dagbag = DagBag()
    assert len(dagbag.import_errors) == 0
