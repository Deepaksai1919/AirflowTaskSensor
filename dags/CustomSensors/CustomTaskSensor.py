from airflow.sensors.external_task import ExternalTaskSensor
from airflow.models import DagRun, TaskInstance
from sqlalchemy import func
from datetime import datetime


class CustomExternalTaskSensor(ExternalTaskSensor):
    def __init__(
            self,
            external_dag_id,
            external_task_id=None,
            allowed_states=None,
            failed_states=None,
            execution_delta=None,
            execution_date_fn=None,
            check_existence=False,
            **kwargs,
    ):
        super(CustomExternalTaskSensor, self).__init__(
            external_dag_id=external_dag_id,
            external_task_id=external_task_id,
            allowed_states=allowed_states,
            failed_states=failed_states,
            execution_delta=execution_delta,
            execution_date_fn=execution_date_fn,
            check_existence=check_existence,
            **kwargs
        )

    def get_count(self, dttm_filter, session, states) -> int:
        """
            This method can be modified to query the task_instance table of airflow as per the requirement.
            Here we wanted to check for the dag run where execution_date >= dttm_filter[0] and execution_date <= dttm_filter[1].
            The values of the dttm_filter are returned by the execution_date_fn argument of the Sensor.
            TI is the class sqlalchemy.orm.attributes.InstrumentedAttribute and hence it's mentods can be utilized as per the requirement
        """
        TI = TaskInstance
        DR = DagRun
        if self.external_task_id:
            count = (
                session.query(func.count())
                    .filter(
                    TI.dag_id == self.external_dag_id,
                    TI.task_id == self.external_task_id,
                    TI.state.in_(states),
                    TI.execution_date.__ge__(datetime.fromisoformat(dttm_filter[0].isoformat())),
                    TI.execution_date.__le__(datetime.fromisoformat(dttm_filter[1].isoformat())),
                ).scalar()
            )
        else:
            count = (
                session.query(func.count())
                    .filter(
                    DR.dag_id == self.external_dag_id,
                    DR.state.in_(states),
                    DR.execution_date.in_(dttm_filter),
                ).scalar()
            )
        return count