import asyncio
import logging

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
    logger.info(f"New connection | conn_id: {client_session.id}")
    try:
        while True:
            message = await websocket.recv()
            logger.info(
                f"New message from connection | conn_id: {client_session.id} | message: {message}"
            )
            await relay.handle(client_session, message)
    except:
        logger.error(f"Connection error | conn_id: {client_session.id}", exc_info=True)
    finally:
        logger.info(f"Connection closed | conn_id: {client_session.id}")
        client_session.close()


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    start_websocket_server = websockets.serve(handler, "", 8001)
    event_loop.run_until_complete(start_websocket_server)
    event_loop.run_forever()
