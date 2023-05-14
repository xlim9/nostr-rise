import logging
import uuid
from .model import Close, Event, Request


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, websocket, private_key: str, public_key: str) -> None:
        self.websocket = websocket
        self._private_key = private_key
        self._public_key = public_key
        self._id = str(uuid.uuid4())

    async def publish_event(self, content: str, kind: int = 1) -> str:
        event = Event(content=content, kind=kind, public_key=self._public_key)
        event.sign(private_key=self._private_key)
        message = event.to_client_message()
        await self.websocket.send(message)
        return message

    async def close_subscription(self, subscription_id: str) -> None:
        close = Close(subscription_id)
        message = close.to_message()
        await self.websocket.send(message)
        logger.info(f"Message sent: {message}")

    async def add_subscription(self, subscription_id: str) -> None:
        request = Request(subscription_id)
        message = request.to_message()
        await self.websocket.send(message)
        logger.info(f"Message sent: {message}")

    async def receive(self) -> str:
        message = await self.websocket.recv()
        return message
