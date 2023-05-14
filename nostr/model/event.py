import time
import json
import secp256k1
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Optional
from hashlib import sha256

from .message_type import ClientMessageType, RelayMessageType


class EventKind(IntEnum):
    SET_METADATA = 0
    TEXT_NOTE = 1
    RECOMMEND_RELAY = 2


@dataclass
class Event:
    content: str
    public_key: str
    created_at: int = int(time.time())
    kind: int = EventKind.TEXT_NOTE
    tags: List[List[str]] = field(default_factory=list)
    signature: Optional[str] = None

    def verify(self, private_key: str):
        sk = secp256k1.PrivateKey(bytes.fromhex(private_key))
        sig = sk.schnorr_sign(bytes.fromhex(self.id), None, raw=True)
        self.signature = sig.hex()

    @staticmethod
    def serialize(
        public_key: str, created_at: int, kind: int, tags: List[List[str]], content: str
    ) -> bytes:
        data = [0, public_key, created_at, kind, tags, content]
        data_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        return data_str.encode()

    @staticmethod
    def _id(
        public_key: str, created_at: int, kind: int, tags: List[List[str]], content: str
    ):
        return sha256(
            Event.serialize(public_key, created_at, kind, tags, content)
        ).hexdigest()

    @property
    def id(self) -> str:
        return Event._id(
            self.public_key, self.created_at, self.kind, self.tags, self.content
        )

    def to_client_message(self) -> str:
        return json.dumps(
            [
                ClientMessageType.EVENT,
                {
                    "id": self.id,
                    "pubkey": self.public_key,
                    "created_at": self.created_at,
                    "kind": self.kind,
                    "tags": self.tags,
                    "content": self.content,
                    "sig": self.signature,
                },
            ]
        )

    def to_relay_message(self, subscription_id: str) -> str:
        return json.dumps(
            [
                RelayMessageType.EVENT,
                subscription_id,
                {
                    "id": self.id,
                    "pubkey": self.public_key,
                    "created_at": self.created_at,
                    "kind": self.kind,
                    "tags": self.tags,
                    "content": self.content,
                    "sig": self.signature,
                },
            ]
        )

    @classmethod
    def from_client_message(cls, message: str):
        parsed = json.loads(message)
        event_json = parsed[1]
        return cls(
            content=event_json["content"],
            public_key=event_json["pubkey"],
            created_at=event_json["created_at"],
            kind=event_json["kind"],
            tags=event_json["tags"],
            signature=event_json["sig"],
        )
