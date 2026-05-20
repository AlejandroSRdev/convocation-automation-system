import datetime
from dataclasses import dataclass, field


@dataclass
class PlayerRenderDTO:
    number: int | None
    name: str
    innings: str
    category_badge: str | None


@dataclass
class InvitedPlayerRenderDTO:
    number: int | None
    name: str
    innings: str


@dataclass
class StaffRenderDTO:
    role: str
    name: str


@dataclass
class ConvocationRenderDTO:
    home_team: str
    away_team: str
    matchday: int
    match_date: datetime.date
    match_time: datetime.time
    convocation_time: str
    location: str
    competition_type: str
    players: list[PlayerRenderDTO] = field(default_factory=list)
    invited_players: list[InvitedPlayerRenderDTO] = field(default_factory=list)
    staff: list[StaffRenderDTO] = field(default_factory=list)
    manual_notes: list[str] = field(default_factory=list)
