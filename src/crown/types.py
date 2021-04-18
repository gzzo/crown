import asyncio
import enum
from pydantic import BaseModel
from typing import Dict, Union, List, Optional, Any


class TaskBody(BaseModel):
    name: str
    args: List[Any]
    queue: Optional[str]


DEFAULT_QUEUE = "DEFAULT"

Results = Dict[str, asyncio.Queue]
Tasks = Dict[str, Any]
