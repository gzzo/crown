import asyncio
from structlog import get_logger
from typing import Coroutine

from .task import Task
from .types import Results

log = get_logger()


class TaskQueue(object):
    def __init__(self, results: Results) -> None:
        self.queue: asyncio.Queue[Task] = asyncio.Queue()
        self.results = results

    def put_task(self, task: Task) -> None:
        log.info("Queueing task", task=task)
        self.results[task.id] = asyncio.Queue()
        return self.queue.put_nowait(task)

    def get_task(self) -> Coroutine[None, None, Task]:
        return self.queue.get()
