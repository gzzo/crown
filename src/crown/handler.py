from typing import Any, Callable

from .task import Task
from .queue import TaskQueue
from .types import Results, Tasks


class TaskHandler(object):
    def __init__(self, name: str, func: Callable, tasks: Tasks, results: Results, queue: TaskQueue) -> None:
        self.name = name
        self.func = func
        self.results = results
        self.queue = queue
        tasks[name] = self

    async def __call__(self, *args: Any) -> Any:
        return await self.func(*args)

    async def get(self, *args: Any) -> Any:
        task = Task(self.name, args, queue_name=self.queue.name)
        self.queue.put_task(task)

        return await self.results[task.id].get()
