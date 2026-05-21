from dataclasses import dataclass


@dataclass
class Player:
    id: int
    number: int | None
    name: str
    category_badge: str | None
    active: bool
