import logging
from typing import Collection, Dict
from .model import Event


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class Database:
    async def add(self, event: Event) -> None:
        pass

    async def query(self) -> Collection[Event]:
        pass


class InMemoryDatabase:
    def __init__(self):
        self.db: Dict[str, Event] = {}

    async def add(self, event: Event) -> None:
        self.db[event.id] = event

    async def query(self) -> Collection[Event]:
        return list(self.db.values())
