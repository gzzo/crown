from typing import Iterable, Any
from uuid import uuid4
from structlog import get_logger

log = get_logger()


class Task(object):
    def __init__(self, name: str, args: Iterable[Any]) -> None:
        self.name = name
        self.args = args
        self.id = str(uuid4())

    def __repr__(self) -> str:
        return f"<Task name={self.name} args={self.args} id={self.id}>"

