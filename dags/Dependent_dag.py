from airflow import DAG
from airflow.operators.python import PythonOperator
from CustomSensors.CustomTaskSensor import CustomExternalTaskSensor
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 10, 11, 1, 0, 0),
    'depends_on_past': False
}


def hello_world_py(*args):
    print('Dependency met!')


dependent_dag = DAG('dependent_dag', schedule_interval='0 0 * * *', default_args=default_args)


t1 = CustomExternalTaskSensor(
    task_id='task1',
    external_dag_id='main_dag',
    external_task_id='hello_world',
    dag=dependent_dag,
    execution_date_fn=lambda dt: [datetime.fromisoformat('2021-10-14T00:00:00 +00:00'), datetime.fromisoformat('2021-10-14T03:00:00 +00:00')]
)

t2 = PythonOperator(task_id='task2', python_callable=hello_world_py, dag=dependent_dag)

t2.set_upstream(t1)