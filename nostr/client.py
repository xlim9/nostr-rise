import ssl
import logging
import threading
import time
import uuid
from threading import Lock

from websocket import WebSocketApp

from .model.close import Close
from .model.event import Event
from .model.request import Request


logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, url: str, private_key: str):
        self._url = url
        self._private_key = private_key
        self._id = str(uuid.uuid4())
        self.lock: Lock = Lock()
        self.ws: WebSocketApp = WebSocketApp(
            self._url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

    def open_connection(self):
        threading.Thread(target=self._connect, name=f"{self._url}-thread").start()
        time.sleep(1)

    def close_connection(self):
        self.ws.close()

    def _connect(self):
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def _publish(self, message: str):
        self.ws.send(message)

    def add_subscription(self):
        with self.lock:
            request = Request(self._id)
            message = request.to_message()
            logger.debug(f"Client message: {message}")
            self._publish(message)

    def close_subscription(self) -> None:
        with self.lock:
            close = Close(self._id)
            message = close.to_message()
            logger.debug(f"Client message: {message}")
            self._publish(message)

    def publish_event(self, event: Event):
        event.verify(private_key=self._private_key)
        message = event.to_client_message()
        logger.debug(f"Client message: {message}")
        self._publish(message)

    def _on_open(self, class_obj):
        pass

    def _on_close(self, class_obj, status_code, message):
        pass

    def _on_message(self, class_obj, message: str):
        logger.info(f"Message received: {message}")

    def _on_error(self, class_obj, error):
        logger.error(f"Client error: {error}")
