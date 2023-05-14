import json
from dataclasses import dataclass

from .message_type import ClientMessageType


@dataclass
class Request:
    id: str

    def to_message(self) -> str:
        message = [ClientMessageType.REQUEST, self.id]
        return json.dumps(message)

    @classmethod
    def from_message(cls, message: str):
        parsed = json.loads(message)
        return cls(parsed[1])
