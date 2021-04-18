from typing import Callable, Any, Dict
from structlog import get_logger
from collections import defaultdict

from .handler import TaskHandler
from .queue import TaskQueue
from .task import Task, TaskStatus
from .types import Tasks, Results, QueueName, QueueNameType, TaskBody

log = get_logger()


class Crown(object):
    def __init__(self) -> None:
        self.tasks: Tasks = {}
        self.results: Results = {}
        self.queues: Dict[QueueNameType, TaskQueue] = {QueueName.DEFAULT: TaskQueue(self.results)}
        self.queue = self.queues[QueueName.DEFAULT]

    def task(self, name: str, queue_name: QueueNameType = QueueName.DEFAULT) -> Callable[[Callable], TaskHandler]:
        def decorator(func: Callable) -> TaskHandler:
            if queue_name not in self.queues:
                self.queues[queue_name] = TaskQueue(self.results, name=queue_name)
            handler = TaskHandler(name, func, self.tasks, self.results, self.queues[queue_name])
            return handler

        return decorator

    def create_and_queue_task(self, task_body: TaskBody) -> None:
        queue_name: str = task_body.queue
        if not queue_name:
            queue_name = self.tasks[task_body.name].queue.name
        task = Task(task_body.name, task_body.args, queue_name=queue_name)
        self.queues[queue_name].put_task(task)

    async def process_task(self, task: Task) -> Any:
        log.info("Processing task", task=task)

        task.status = TaskStatus.ACTIVE
        result = await self.tasks[task.name](*task.args)
        self.results[task.id].put_nowait(result)
        self.queues[task.queue_name].active.remove(task)
        task.status = TaskStatus.DONE

        log.info("Success processing task", task=task, result=result)
        return result
