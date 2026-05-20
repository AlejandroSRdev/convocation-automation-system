import datetime
from dataclasses import dataclass


@dataclass
class Match:
    id: int
    home_team: str
    away_team: str
    matchday: int
    match_date: datetime.date
    match_time: datetime.time
    location: str
    competition_type: str
