import logging
from dataclasses import dataclass

from app.application.ports.player_repository import PlayerRepository
from app.domain.entities.player import Player

logger = logging.getLogger(__name__)


@dataclass
class GetPlayersResult:
    players: list[Player]


class GetPlayersUseCase:
    def __init__(self, player_repository: PlayerRepository) -> None:
        self._player_repo = player_repository

    def execute(self) -> GetPlayersResult:
        logger.info("get_players.started")
        players = self._player_repo.get_active()
        logger.info("get_players.completed", extra={"count": len(players)})
        return GetPlayersResult(players=players)
