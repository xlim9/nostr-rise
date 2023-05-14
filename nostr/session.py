import uuid
from typing import Any, Callable, Optional


class ClientSession:
    def __init__(self, websocket) -> None:
        self._closed = False
        self._on_close: Optional[Callable] = None
        self.websocket = websocket
        self.id = str(uuid.uuid4())

    @property
    def on_close(self) -> Callable[[], Any]:
        if self._on_close:
            return self._on_close
        return lambda: None

    @on_close.setter
    def on_close(self, func: Callable[[], None]) -> None:
        self._on_close = func

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self.on_close()

    async def send(self, message: str) -> None:
        if self._closed:
            return
        await self.websocket.send(message)
