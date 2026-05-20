import logging
from dataclasses import dataclass

from app.application.ports.match_repository import MatchRepository
from app.domain.entities.match import Match

logger = logging.getLogger(__name__)


@dataclass
class GetMatchesResult:
    matches: list[Match]


class GetMatchesUseCase:
    def __init__(self, match_repository: MatchRepository) -> None:
        self._match_repo = match_repository

    def execute(self) -> GetMatchesResult:
        logger.info("get_matches.started")
        matches = self._match_repo.get_all()
        logger.info("get_matches.completed", extra={"count": len(matches)})
        return GetMatchesResult(matches=matches)
