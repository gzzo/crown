import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, List
from structlog import get_logger

from .crown import Crown
from .task import Task

log = get_logger()
app = FastAPI(debug=True)
crown = Crown()


async def worker() -> None:
    log.msg("Starting worker")
    while True:
        task: Task = await crown.queue.get_task()
        await crown.process_task(task)


class TaskBody(BaseModel):
    name: str
    args: List[Any]


@app.post('/create')
async def create(task_body: TaskBody) -> Any:
    task = Task(task_body.name, task_body.args)
    crown.queue.put_task(task)

    return {'success': True}


@app.on_event('startup')
async def work() -> None:
    asyncio.create_task(worker())
    asyncio.create_task(worker())


@crown.task('add')
async def add(a: int, b: int) -> int:
    return a + b


@crown.task('square')
async def square(a: int) -> int:
    total = 0
    for _ in range(a):
        total = await add.get(total, a)

    return abs(total)
