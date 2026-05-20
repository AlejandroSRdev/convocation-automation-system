from sqlalchemy.orm import Session

from app.domain.entities.match import Match
from app.infrastructure.database.models.match import MatchModel


class SQLMatchRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, match_id: int) -> Match | None:
        model = self._session.get(MatchModel, match_id)
        if model is None:
            return None
        return Match(
            id=model.id,
            home_team=model.home_team,
            away_team=model.away_team,
            matchday=model.matchday,
            match_date=model.match_date,
            match_time=model.match_time,
            location=model.location,
            competition_type=model.competition_type,
        )

    def get_all(self) -> list[Match]:
        models = self._session.query(MatchModel).all()
        return [
            Match(
                id=model.id,
                home_team=model.home_team,
                away_team=model.away_team,
                matchday=model.matchday,
                match_date=model.match_date,
                match_time=model.match_time,
                location=model.location,
                competition_type=model.competition_type,
            )
            for model in models
        ]
