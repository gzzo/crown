import enum
from typing import Iterable, Any
from uuid import uuid4
from structlog import get_logger

from .types import QueueName, QueueNameType

log = get_logger()


class TaskStatus(enum.Enum):
    CREATED = 'CREATED'
    QUEUED = 'QUEUED'
    ACTIVE = 'ACTIVE'
    DONE = 'DONE'


class Task(object):
    def __init__(self, name: str, args: Iterable[Any], queue_name: QueueNameType = QueueName.DEFAULT) -> None:
        self.name = name
        self.args = args
        self.id = str(uuid4())
        self.status = TaskStatus.CREATED
        self.queue_name = queue_name

    def __repr__(self) -> str:
        return f"<Task status={self.status} name={self.name} args={self.args} queue={self.queue_name} id={self.id}>"
