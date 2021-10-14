# AirflowTaskSensor
#### A sensor similar to airflow ExternalTaskSensor

Airflow's ExternalTaskSensor can be used to monitor a task of another dag and establish a dependency on it. But it will work only for dags which are scheduled.

CustomTaskSensor inherits the methods of `ExternalTaskSensor` and overrides the `get_count` method so that this sensor can be used to establish a dependency on dags  which have `None` schedule.

## Example:
Two sample dags (main_dag & dependent_dag) are included in the repo.
```python
main_dag = DAG('main_dag', schedule_interval=None, default_args=default_args)
```
```python
dependent_dag = DAG('dependent_dag', schedule_interval='0 0 * * *', default_args=default_args)
```

main_dag has None schedule where as the dependent_dag has schedule `0 0 * * *`

```python
execution_date_fn = lambda dt: [datetime.fromisoformat('2021-10-14T00:00:00 +00:00'), datetime.fromisoformat('2021-10-14T03:00:00 +00:00')]
```
A list of two timestamps are passed in the example so the dependent_dag monitors the run of main_dag in the interval `2021-10-14T00:00:00 +00:00` and `2021-10-14T03:00:00 +00:00`. These values can be passed dynamically using the macros and timedelta.

The arguments passed will be converted in an sql query which will be equivalent to

```SQL
SELECT count(*) AS count_1
FROM task_instance
WHERE task_instance.dag_id = 'main_dag' 
AND task_instance.task_id = 'hello_world' 
AND task_instance.execution_date >= '2021-10-14T00:00:00 +00:00' 
AND task_instance.execution_date <= '2021-10-14T03:00:00 +00:00'
```

Other column values can also be used as per the requirement.

Below is the list of columns in the task_instance table.
|table|	column	|data type|
| :---        |    :----:   |          ---: |
task_instance|task_id|character varying|
|task_instance|dag_id|character varying|
|task_instance|execution_date|timestamp with time zone|
|task_instance|start_date|timestamp with time zone|
|task_instance|end_date|timestamp with time zone|
|task_instance|duration|double precision|
|task_instance|state|character varying|
|task_instance|try_number|integer|
|task_instance|hostname|character varying|
|task_instance|unixname|character varying|
|task_instance|job_id|integer|
|task_instance|pool|character varying|
|task_instance|queue|character varying|
|task_instance|priority_weight|integer|
|task_instance|operator|character varying|
|task_instance|queued_dttm|timestamp with time zone|
|task_instance|pid|integer|
|task_instance|max_tries|integer|
|task_instance|executor_config|bytea|
|task_instance|pool_slots|integer|
|task_instance|queued_by_job_id|integer|
|task_instance|external_executor_id|character varying