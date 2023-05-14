import json
import logging
from typing import Collection
from .model import ClientMessageType, Event, Request, Subscriptions
from .database import Database, InMemoryDatabase
from .session import ClientSession


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class Relay:
    def __init__(self):
        self._db: Database = InMemoryDatabase()
        self._subscriptions: Subscriptions = Subscriptions()

    def _parse_message_type(self, message: str) -> ClientMessageType:
        parsed = json.loads(message)
        return parsed[0]

    async def _send_db_events(
        self,
        client_session: ClientSession,
        subscription_id: str,
        events: Collection[Event],
    ) -> None:
        if not events:
            return

        for event in events:
            message = event.to_relay_message(subscription_id=subscription_id)
            await client_session.send(message)

    async def handle(self, client_session: ClientSession, message: str):
        message_type = self._parse_message_type(message)
        if message_type == ClientMessageType.EVENT:
            event = Event.from_client_message(message)
            await self._db.add(event)
            await self._subscriptions.broadcast(event)
        elif message_type == ClientMessageType.REQUEST:
            request = Request.from_message(message)
            events = await self._db.query()
            await self._send_db_events(
                client_session=client_session, subscription_id=request.id, events=events
            )
            self._subscriptions.subscribe(id=request.id, client_session=client_session)
        elif message_type == ClientMessageType.CLOSE:
            self._subscriptions.unsubscribe(id=request.id)
        else:
            raise TypeError(f"Message type {message_type} is not supported")
