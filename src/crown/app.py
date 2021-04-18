import asyncio
import uvicorn  # type: ignore
from fastapi import FastAPI
from typing import Any, Set
from structlog import get_logger

from .crown import Crown
from .task import Task
from .types import TaskBody

log = get_logger()
app = FastAPI(debug=True)
crown = Crown()


async def worker(queue_name: str) -> None:
    log.msg("Starting worker", queue_name=queue_name)
    while True:
        task: Task = await crown.queues[queue_name].get_task()
        await crown.process_task(task)


@app.post('/create')
async def create(task_body: TaskBody) -> Any:
    crown.create_and_queue_task(task_body)

    return {'success': True}


@app.get('/processing')
async def processing() -> Set[Task]:
    return crown.queue.active


@app.on_event('startup')
async def work() -> None:
    for queue_name in crown.queues.keys():
        asyncio.create_task(worker(queue_name))
        asyncio.create_task(worker(queue_name))


@crown.task('add')
async def add(a: int, b: int) -> int:
    await asyncio.sleep(10)
    return a + b


@crown.task('square', queue_name='square_queue')
async def square(a: int) -> int:
    total = 0
    for _ in range(a):
        total = await add.get(total, a)

    return abs(total)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)
