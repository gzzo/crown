from typing import Callable, Any
from structlog import get_logger

from .handler import TaskHandler
from .queue import TaskQueue
from .task import Task
from .types import Tasks, Results

log = get_logger()


class Crown(object):
    def __init__(self) -> None:
        self.tasks: Tasks = {}
        self.results: Results = {}
        self.queue = TaskQueue(self.results)

    def task(self, name: str) -> Callable[[Callable], TaskHandler]:
        def decorator(func: Callable) -> TaskHandler:
            return TaskHandler(name, func, self.tasks, self.results, self.queue)

        return decorator

    async def process_task(self, task: Task) -> Any:
        log.info("Processing task", task=task)

        result = await self.tasks[task.name](*task.args)
        self.results[task.id].put_nowait(result)

        log.info("Success processing task", task=task, result=result)
        return result
