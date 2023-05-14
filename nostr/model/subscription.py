from dataclasses import dataclass
from collections import UserDict

from ..session import ClientSession
from .message import Event


@dataclass
class Subscription:
    id: str
    client_session: ClientSession

    async def update(self, event: Event) -> None:
        message = event.to_relay_message(subscription_id=self.id)
        await self.client_session.send(message)


class Subscriptions(UserDict[str, Subscription]):
    def subscribe(self, id: str, client_session: ClientSession) -> None:
        self[id] = Subscription(id, client_session)
        client_session.on_close = lambda: self.pop(id, None)

    def unsubscribe(self, id: str) -> None:
        del self[id]

    async def broadcast(self, event: Event) -> None:
        for subscription in self.values():
            await subscription.update(event)
