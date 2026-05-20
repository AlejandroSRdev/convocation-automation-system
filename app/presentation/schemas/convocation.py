import uuid

from pydantic import BaseModel


class RefineConvocationRequest(BaseModel):
    message: str
    critical_fragments: list[str]
    style: str | None = None


class RefineConvocationResponse(BaseModel):
    refined_message: str
    was_refined: bool


class InvitedPlayerInput(BaseModel):
    name: str
    number: int | None = None


class GenerateConvocationRequest(BaseModel):
    match_id: int
    convocation_time: str
    selected_staff_ids: list[uuid.UUID] = []
    player_innings: dict[str, str] = {}
    excluded_player_ids: list[uuid.UUID] = []
    invited_players: list[InvitedPlayerInput] = []
    manual_notes: list[str] = []


class PlayerInfo(BaseModel):
    number: int | None
    name: str
    innings: str
    category_badge: str | None


class StaffInfo(BaseModel):
    role: str
    name: str


class MatchInfo(BaseModel):
    home_team: str
    away_team: str
    matchday: int
    match_date: str
    match_time: str
    location: str
    competition_type: str


class GenerateConvocationResponse(BaseModel):
    rendered_message: str
    match_metadata: MatchInfo
    selected_players: list[PlayerInfo]
    selected_staff: list[StaffInfo]
    critical_fragments: list[str]
