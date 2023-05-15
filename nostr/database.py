import logging
import sqlite3
from typing import Collection, Dict

import aiosqlite

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
        self._database: Dict[str, Event] = {}

    async def add(self, event: Event) -> None:
        self._database[event.id] = event

    async def query(self) -> Collection[Event]:
        return list(self._database.values())


class SQLiteDatabase:
    def __init__(self):
        database = sqlite3.connect("test.db")
        database.execute("CREATE TABLE IF NOT EXISTS events (id TEXT, message TEXT)")
        database.close()

    async def add(self, event: Event) -> None:
        id = event.id
        message = event.to_client_message()
        query = f"INSERT INTO events(id, message) VALUES ('{id}', '{message}')"
        db = await aiosqlite.connect("test.db")
        await db.execute(query)
        await db.commit()
        await db.close()

    async def query(self) -> Collection[Event]:
        db = await aiosqlite.connect("test.db")
        results = []
        async with db.execute("SELECT message FROM events") as cursor:
            async for row in cursor:
                results.append(Event.from_client_message(row[0]))
        return results
