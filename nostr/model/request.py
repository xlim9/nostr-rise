import json
from dataclasses import dataclass

from .message_type import ClientMessageType
from .subscription import Subscription

@dataclass
class Request:
    subscription: Subscription

    def to_message(self) -> str:
        message = [ClientMessageType.REQUEST, self.subscription.id]
        return json.dumps(message)