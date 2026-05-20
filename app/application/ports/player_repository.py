from typing import Protocol

from app.domain.entities.player import Player


class PlayerRepository(Protocol):
    def get_active(self) -> list[Player]: ...
