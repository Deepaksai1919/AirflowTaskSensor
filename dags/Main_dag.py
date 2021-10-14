from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 10, 11, 1, 0, 0)
}


def hello_world_py(*args):
    print('Hello World')


main_dag = DAG('main_dag', schedule_interval=None, default_args=default_args)

with main_dag:
    t1 = PythonOperator(task_id='hello_world', python_callable=hello_world_py)
