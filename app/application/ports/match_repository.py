import uuid
from typing import Protocol

from app.domain.entities.match import Match


class MatchRepository(Protocol):
    def get_by_id(self, match_id: uuid.UUID) -> Match | None: ...
    def get_all(self) -> list[Match]: ...
