import json
from dataclasses import dataclass

from .message_type import ClientMessageType
from .subscription import Subscription

@dataclass
class Close:
    subscription: Subscription

    def to_message(self) -> str:
        message = [ClientMessageType.CLOSE, self.subscription.id]
        return json.dumps(message)

    @classmethod
    def from_message(cls, message: str):
        parsed = json.loads(message)
        subscription = Subscription(parsed[1])
        return cls(subscription)

    @property
    def id(self) -> str:
        return self.subscription.id