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


class InMemoryDatabase(Database):
    def __init__(self):
        self._database: Dict[str, Event] = {}

    async def add(self, event: Event) -> None:
        self._database[event.id] = event

    async def query(self) -> Collection[Event]:
        return list(self._database.values())


class SQLiteDatabase(Database):
    def __init__(self, db_name: str):
        self.db_name = db_name
        database = sqlite3.connect(self.db_name)
        database.execute("CREATE TABLE IF NOT EXISTS events (id TEXT, message TEXT)")
        database.close()

    async def add(self, event: Event) -> None:
        id = event.id
        message = event.to_client_message()
        message = message.replace("'", "''")
        query = f"INSERT INTO events(id, message) VALUES ('{id}', '{message}')"
        db = await aiosqlite.connect(self.db_name)
        await db.execute(query)
        await db.commit()
        await db.close()

    async def query(self) -> Collection[Event]:
        db = await aiosqlite.connect(self.db_name)
        results = []
        async with db.execute("SELECT message FROM events") as cursor:
            async for row in cursor:
                results.append(Event.from_client_message(row[0]))
        return results
