import asyncio
import enum
from pydantic import BaseModel
from typing import Dict, Union, List, Optional, Any


class QueueName(enum.Enum):
    DEFAULT = 'DEFAULT'


class TaskBody(BaseModel):
    name: str
    args: List[Any]
    queue: Optional[str]


Results = Dict[str, asyncio.Queue]
QueueNameType = Union[str, QueueName]
Tasks = Dict[str, Any]
