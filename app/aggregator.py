import asyncio
import logging
import uuid

import aio_pika
import json
import websockets
from nostr import Client
from nostr.database import SQLiteDatabase
from nostr.model import Event, RelayMessageType

PRIVATE_KEY = "ca52acacfbfbf9f040de69361a2c1ea78b705399ce909d4a5a87e7bc029cead7"
PUBLIC_KEY = "d0b69840e1a7f1f19a4227c0311ffd42e28ddd277b2e259fb64e6a2e559bb408"
SUBSCRIPTION_ID = str(uuid.uuid4())


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("aiosqlite").propagate = False
logging.getLogger("aiormq").propagate = False
logging.getLogger("aio_pika").propagate = False
logger = logging.getLogger("AGGREGATOR CLIENT")


db = SQLiteDatabase("aggregator.db")


async def aggregator(HOST) -> None:
    async with websockets.connect(HOST) as websocket:
        client = Client(websocket, private_key=PRIVATE_KEY, public_key=PUBLIC_KEY)
        await client.add_subscription(SUBSCRIPTION_ID)
        logger.info(f"Subscription added | subscription_id: {SUBSCRIPTION_ID}")
        try:
            while True:
                message = await client.receive()
                logger.info(f"Message received | message: {message}")

                queue_connection = await aio_pika.connect_robust(
                    "amqp://guest:guest@127.0.0.1/",
                )
                async with queue_connection:
                    channel = await queue_connection.channel()
                    await channel.default_exchange.publish(
                        aio_pika.Message(body=message.encode("utf-8")),
                        routing_key="messages",
                    )
                    logger.info(f"Message published to queue | message: {message}")
        except:
            await client.close_subscription(SUBSCRIPTION_ID)
            logger.info(f"Subscription closed | subscription_id: {SUBSCRIPTION_ID}")


async def consumer() -> None:
    logging.basicConfig(level=logging.INFO)
    queue_connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )
    async with queue_connection:
        channel = await queue_connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue("messages", auto_delete=True)
        async with queue.iterator() as queue_iter:
            async for item in queue_iter:
                async with item.process():
                    message = item.body.decode("utf-8")
                    parsed = json.loads(message)
                    if parsed[0] == RelayMessageType.EVENT:
                        logger.info(f"Message received from queue | message: {message}")
                        event = Event.from_relay_message(message)
                        event.verify()
                        await db.add(event)
                        logger.info(f"Message saved to database | message: {message}")


async def events():
    events = await db.query()
    logger.info(f"Events in database: {events}")


async def main():
    await asyncio.gather(
        aggregator("wss://nostr-rise.herokuapp.com/"),
        aggregator("wss://relay.nekolicio.us/"),
        consumer(),
    )


if __name__ == "__main__":
    asyncio.run(main())
