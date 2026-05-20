import uuid
import datetime

from pydantic import BaseModel


class MatchResponse(BaseModel):
    id: uuid.UUID
    home_team: str
    away_team: str
    matchday: int
    match_date: datetime.date
    match_time: datetime.time
    location: str
    competition_type: str
