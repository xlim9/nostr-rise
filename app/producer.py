import asyncio
import logging

import websockets
from nostr import Client, Event

WS_LOCALHOST = "ws://0.0.0.0:8001"
PRIVATE_KEY = "ca52acacfbfbf9f040de69361a2c1ea78b705399ce909d4a5a87e7bc029cead7"
PUBLIC_KEY = "d0b69840e1a7f1f19a4227c0311ffd42e28ddd277b2e259fb64e6a2e559bb408"


logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger("PRODUCER CLIENT")


async def producer() -> None:
    async with websockets.connect(WS_LOCALHOST) as websocket:
        client = Client(websocket, private_key=PRIVATE_KEY)
        event = Event(
            content="hello",
            kind=1,
            public_key=PUBLIC_KEY,
        )
        await client.publish_event(event)
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(producer())
