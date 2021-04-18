import asyncio
from typing import Dict, Callable

Tasks = Dict[str, Callable]
Results = Dict[str, asyncio.Queue]
