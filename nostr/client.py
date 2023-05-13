import ssl
import logging
import threading
import time
from threading import Lock
from typing import Dict

from websocket import WebSocketApp

from .model.close import Close
from .model.event import Event
from .model.request import Request
from .model.subscription import Subscription


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, url):
        self.url = url
        self.subscriptions: Dict[str, Subscription] = {}
        self.lock: Lock = Lock()
        self.ws: WebSocketApp = WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

    def open_connection(self):
        threading.Thread(target=self._connect, name=f"{self.url}-thread").start()
        time.sleep(1)

    def close_connection(self):
        self.ws.close()

    def _connect(self):
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def _publish(self, message: str):
        self.ws.send(message)

    def add_subscription(self, id):
        with self.lock:
            subscription = Subscription(id)
            self.subscriptions[id] = subscription
            request = Request(subscription)
            message = request.to_message()
            logger.debug(f"Client message: {message}")
            self._publish(request.to_message())

    def close_subscription(self, id: str) -> None:
        with self.lock:
            subscription = Subscription(id)
            close = Close(subscription)
            message = close.to_message()
            logger.debug(f"Client message: {message}")
            self._publish(message)
            self.subscriptions.pop(id, None)

    def publish_event(self, event: Event):
        message = event.to_message()
        logger.debug(f"Client message: {message}")
        self._publish(message)

    def _on_open(self, class_obj):
        pass

    def _on_close(self, class_obj, status_code, message):
        pass

    def _on_message(self, class_obj, message: str):
        pass

    def _on_error(self, class_obj, error):
        pass
