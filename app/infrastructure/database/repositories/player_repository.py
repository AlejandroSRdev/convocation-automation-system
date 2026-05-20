from sqlalchemy.orm import Session

from app.domain.entities.player import Player
from app.infrastructure.database.models.player import PlayerModel


class SQLPlayerRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_active(self) -> list[Player]:
        models = (
            self._session.query(PlayerModel)
            .filter(PlayerModel.active == True)
            .all()
        )
        return [
            Player(
                id=m.id,
                number=m.number,
                name=m.name,
                category_badge=m.category_badge,
                active=m.active,
            )
            for m in models
        ]
