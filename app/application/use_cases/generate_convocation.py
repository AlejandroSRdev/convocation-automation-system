import datetime
import logging
from dataclasses import dataclass, field

from app.application.ports.match_repository import MatchRepository
from app.application.ports.player_repository import PlayerRepository
from app.application.ports.staff_repository import StaffRepository
from app.application.rendering.convocation_renderer import ConvocationRenderer
from app.application.rendering.dtos import (
    ConvocationRenderDTO,
    PlayerRenderDTO,
    InvitedPlayerRenderDTO,
    StaffRenderDTO,
)
from app.application.rendering.blocks.links_block import get_operational_urls
from app.domain.exceptions import MatchNotFoundError

logger = logging.getLogger(__name__)

DEFAULT_INNINGS = "?/?"


@dataclass
class InvitedPlayerInput:
    name: str
    number: int | None = None


@dataclass
class GenerateConvocationCommand:
    match_id: int
    convocation_time: str
    selected_staff_ids: list[int] = field(default_factory=list)
    player_innings: dict[int, str] = field(default_factory=dict)
    excluded_player_ids: list[int] = field(default_factory=list)
    invited_players: list[InvitedPlayerInput] = field(default_factory=list)
    manual_notes: list[str] = field(default_factory=list)


@dataclass
class GenerateConvocationResult:
    rendered_message: str
    home_team: str
    away_team: str
    matchday: int
    match_date: datetime.date
    match_time: datetime.time
    location: str
    competition_type: str
    selected_players: list[PlayerRenderDTO]
    selected_staff: list[StaffRenderDTO]
    critical_fragments: list[str]


class GenerateConvocationUseCase:
    def __init__(
        self,
        match_repository: MatchRepository,
        player_repository: PlayerRepository,
        staff_repository: StaffRepository,
        renderer: ConvocationRenderer,
    ) -> None:
        self._match_repo = match_repository
        self._player_repo = player_repository
        self._staff_repo = staff_repository
        self._renderer = renderer

    def execute(self, command: GenerateConvocationCommand) -> GenerateConvocationResult:
        logger.info("generate_convocation.started", extra={"match_id": str(command.match_id)})

        # Step 1: Load match
        match = self._match_repo.get_by_id(command.match_id)
        if match is None:
            raise MatchNotFoundError(str(command.match_id))

        # Step 2: Load and filter active players
        all_active = self._player_repo.get_active()
        excluded_set = set(command.excluded_player_ids)
        selected_players = [p for p in all_active if p.id not in excluded_set]

        # Step 3: Build player render DTOs
        player_dtos = [
            PlayerRenderDTO(
                number=p.number,
                name=p.name,
                innings=command.player_innings.get(p.id, DEFAULT_INNINGS),
                category_badge=p.category_badge,
            )
            for p in selected_players
        ]

        # Step 4: Build invited player render DTOs
        invited_dtos = [
            InvitedPlayerRenderDTO(
                number=inv.number,
                name=inv.name,
                innings=DEFAULT_INNINGS,
            )
            for inv in command.invited_players
        ]

        # Step 5: Load staff
        staff_members = self._staff_repo.get_active_by_ids(command.selected_staff_ids)
        staff_dtos = [StaffRenderDTO(role=s.role, name=s.name) for s in staff_members]

        # Step 6: Build render DTO
        dto = ConvocationRenderDTO(
            home_team=match.home_team,
            away_team=match.away_team,
            matchday=match.matchday,
            match_date=match.match_date,
            match_time=match.match_time,
            convocation_time=command.convocation_time,
            location=match.location,
            competition_type=match.competition_type,
            players=player_dtos,
            invited_players=invited_dtos,
            staff=staff_dtos,
            manual_notes=command.manual_notes,
        )

        # Step 7: Extract critical fragments
        critical_fragments = _extract_critical_fragments(dto)

        # Step 8: Render
        rendered_message = self._renderer.render(dto)

        logger.info("generate_convocation.completed", extra={"match_id": str(command.match_id)})

        return GenerateConvocationResult(
            rendered_message=rendered_message,
            home_team=match.home_team,
            away_team=match.away_team,
            matchday=match.matchday,
            match_date=match.match_date,
            match_time=match.match_time,
            location=match.location,
            competition_type=match.competition_type,
            selected_players=player_dtos,
            selected_staff=staff_dtos,
            critical_fragments=critical_fragments,
        )


def _extract_critical_fragments(dto: ConvocationRenderDTO) -> list[str]:
    fragments = []

    # Operational match facts — formatted exactly as rendered
    fragments.append(dto.match_date.strftime("%d/%m/%Y"))
    fragments.append(dto.match_time.strftime("%H:%M"))
    fragments.append(dto.convocation_time)
    fragments.append(dto.location)
    fragments.append(dto.home_team)
    fragments.append(dto.away_team)

    # Player operational facts
    for p in dto.players:
        fragments.append(p.name)
        if p.number is not None:
            fragments.append(f"#{p.number}")
        fragments.append(p.innings)

    for p in dto.invited_players:
        fragments.append(p.name)
        if p.number is not None:
            fragments.append(f"#{p.number}")
        fragments.append(p.innings)

    # Staff names
    for s in dto.staff:
        fragments.append(s.name)

    # Operational URLs
    fragments.extend(get_operational_urls())

    return [f for f in fragments if f]
