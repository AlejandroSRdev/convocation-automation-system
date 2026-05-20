import uuid
from dataclasses import dataclass


@dataclass
class Player:
    id: uuid.UUID
    number: int | None
    name: str
    category_badge: str | None
    active: bool
