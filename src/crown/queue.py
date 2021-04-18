import asyncio
from structlog import get_logger
from typing import Set, Coroutine

from .task import Task, TaskStatus
from .types import Results, QueueName, QueueNameType

log = get_logger()


class TaskQueue(object):
    def __init__(self, results: Results, name: QueueNameType = QueueName.DEFAULT) -> None:
        self.results = results
        self.name = name

        self.queue: asyncio.Queue[Task] = asyncio.Queue()
        self.active: Set[Task] = set()

    def put_task(self, task: Task) -> None:
        log.info("Queueing task", task=task, queue_name=self.name)
        self.results[task.id] = asyncio.Queue()
        self.active.add(task)
        task.status = TaskStatus.QUEUED
        return self.queue.put_nowait(task)

    def get_task(self) -> Coroutine[None, None, Task]:
        return self.queue.get()
