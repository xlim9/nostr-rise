import asyncio
import logging
import uuid

import websockets
from nostr import Client

WS_LOCALHOST = "ws://0.0.0.0:8001"
PRIVATE_KEY = "ca52acacfbfbf9f040de69361a2c1ea78b705399ce909d4a5a87e7bc029cead7"
PUBLIC_KEY = "d0b69840e1a7f1f19a4227c0311ffd42e28ddd277b2e259fb64e6a2e559bb408"
SUBSCRIPTION_ID = str(uuid.uuid4())


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger("WATCHER CLIENT")


async def watcher() -> None:
    async with websockets.connect(WS_LOCALHOST) as websocket:
        client = Client(websocket, private_key=PRIVATE_KEY)
        await client.add_subscription(SUBSCRIPTION_ID)
        logger.info(f"Subscription added | subscription_id: {SUBSCRIPTION_ID}")
        try:
            while True:
                message = await client.receive()
                logger.info(f"Message received | message: {message}")
        except:
            await client.close_subscription(SUBSCRIPTION_ID)
            logger.info(f"Subscription closed | subscription_id: {SUBSCRIPTION_ID}")


if __name__ == "__main__":
    asyncio.run(watcher())
