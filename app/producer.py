import asyncio
import logging

import websockets
from nostr import Client

HOST = "wss://nostr-rise.herokuapp.com/"
PRIVATE_KEY = "ca52acacfbfbf9f040de69361a2c1ea78b705399ce909d4a5a87e7bc029cead7"
PUBLIC_KEY = "d0b69840e1a7f1f19a4227c0311ffd42e28ddd277b2e259fb64e6a2e559bb408"


logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger("PRODUCER CLIENT")


async def producer() -> None:
    async with websockets.connect(HOST) as websocket:
        client = Client(websocket, private_key=PRIVATE_KEY, public_key=PUBLIC_KEY)
        message = await client.publish_event(content="hello")
        logger.info(f"Message sent | event: {message}")
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(producer())
