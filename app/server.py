import asyncio
import logging
import os
import signal

import websockets

from nostr import Relay
from nostr import ClientSession


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger("RELAY SERVER")
relay = Relay()


async def handler(websocket) -> None:
    client_session = ClientSession(websocket)
    logger.info(f"Connection added | connection_id: {client_session.id}")
    try:
        while True:
            message = await websocket.recv()
            logger.info(
                f"Message received | connection_id: {client_session.id} | message: {message}"
            )
            await relay.handle(client_session, message)
    except:
        client_session.close()
        logger.info(f"Connection closed | connection_id: {client_session.id}")


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(handler, host="", port=int(os.environ["PORT"])):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
