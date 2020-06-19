import random
import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from investing_bot_framework.core.executors.execution_scheduler import ExecutionScheduler, ExecutionTask
from investing_bot_framework.core.utils import TimeUnit


class TestExecutionScheduler(object):

    def setup_method(self) -> None:

        self.execution_task_one = {
            'execution_id': uuid4().__str__(),
            'time_unit': TimeUnit.ALWAYS,
        }

        self.execution_task_two = {
            'execution_id': uuid4().__str__(),
            'time_unit': TimeUnit.SECOND,
            'interval': random.randint(1, 10),
        }

        self.execution_task_three = {
            'execution_id': uuid4().__str__(),
            'time_unit': TimeUnit.MINUTE,
            'interval': random.randint(1, 10),
        }

        self.execution_task_four = {
            'execution_id': uuid4().__str__(),
            'time_unit': TimeUnit.HOUR,
            'interval': random.randint(1, 10),
        }

        self.wrong_execution_task_one = {
            'execution_id': uuid4().__str__(),
            'time_unit': TimeUnit.HOUR,
            'interval': -1,
        }

        self.wrong_execution_task_two = {
            'execution_id': uuid4().__str__(),
            'time_unit': TimeUnit.HOUR,
        }

    def test(self):
        scheduler = ExecutionScheduler()
        scheduler.add_execution_task(**self.execution_task_one)
        scheduler.add_execution_task(**self.execution_task_two)
        scheduler.add_execution_task(**self.execution_task_three)
        scheduler.add_execution_task(**self.execution_task_four)

        # All tasks must be scheduled the first planning
        planning = scheduler.schedule_executions()
        assert self.execution_task_one['execution_id'] in planning
        assert self.execution_task_two['execution_id'] in planning
        assert self.execution_task_three['execution_id'] in planning
        assert self.execution_task_four['execution_id'] in planning

        # Only Task 1 must be in the planning
        planning = scheduler.schedule_executions()
        assert self.execution_task_one['execution_id'] in planning
        assert self.execution_task_two['execution_id'] not in planning
        assert self.execution_task_three['execution_id'] not in planning
        assert self.execution_task_four['execution_id'] not in planning

        minus_time_delta = datetime.now() - timedelta(seconds=self.execution_task_two['interval'])
        appointments = scheduler._planning.keys()

        # Subtract the interval amount of task 2 in seconds from last execution time
        for appointment in appointments:
            scheduler._planning[appointment] = ExecutionTask(
                scheduler._planning[appointment].time_unit,
                scheduler._planning[appointment].interval,
                last_run=minus_time_delta
            )

        # Task 1, 2 must be in the planning
        planning = scheduler.schedule_executions()
        assert self.execution_task_one['execution_id'] in planning
        assert self.execution_task_two['execution_id'] in planning
        assert self.execution_task_three['execution_id'] not in planning
        assert self.execution_task_four['execution_id'] not in planning

        minus_time_delta = datetime.now() - timedelta(minutes=self.execution_task_three['interval'])
        appointments = scheduler._planning.keys()

        # Subtract the interval amount of task 3 in minutes from last execution time
        for appointment in appointments:
            scheduler._planning[appointment] = ExecutionTask(
                scheduler._planning[appointment].time_unit,
                scheduler._planning[appointment].interval,
                last_run=minus_time_delta
            )

        # Task 1, 2 and 3 must be in the planning
        planning = scheduler.schedule_executions()
        assert self.execution_task_one['execution_id'] in planning
        assert self.execution_task_two['execution_id'] in planning
        assert self.execution_task_three['execution_id'] in planning
        assert self.execution_task_four['execution_id'] not in planning

        minus_time_delta = datetime.now() - timedelta(hours=self.execution_task_four['interval'])
        appointments = scheduler._planning.keys()

        # Subtract the interval amount of task 4 in hours from last execution time
        for appointment in appointments:
            scheduler._planning[appointment] = ExecutionTask(
                scheduler._planning[appointment].time_unit,
                scheduler._planning[appointment].interval,
                last_run=minus_time_delta
            )
        #
        # Task 1, 2 and 3 must be in the planning
        planning = scheduler.schedule_executions()
        assert self.execution_task_one['execution_id'] in planning
        assert self.execution_task_two['execution_id'] in planning
        assert self.execution_task_three['execution_id'] in planning
        assert self.execution_task_four['execution_id'] in planning

    def test_exceptions(self) -> None:
        scheduler = ExecutionScheduler()

        with pytest.raises(Exception) as e_info:
            scheduler.add_execution_task(**self.wrong_execution_task_one)

        assert "Interval for task time unit is smaller then 1" in str(e_info.value)

        with pytest.raises(Exception) as e_info:
            scheduler.add_execution_task(**self.wrong_execution_task_two)

        assert "Appoint must set an interval with the corresponding time unit" in str(e_info.value)

        scheduler.add_execution_task(**self.execution_task_one)

        with pytest.raises(Exception) as e_info:
            scheduler.add_execution_task(**self.execution_task_one)

        assert "Can't add execution task, execution id is already taken" in str(e_info.value)





