from fastapi import APIRouter, Depends

from app.application.use_cases.get_players import GetPlayersUseCase
from app.presentation.dependencies import get_get_players_use_case
from app.presentation.schemas.player import PlayerResponse

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=list[PlayerResponse])
def list_players(
    use_case: GetPlayersUseCase = Depends(get_get_players_use_case),
) -> list[PlayerResponse]:
    result = use_case.execute()
    return [
        PlayerResponse(
            id=player.id,
            name=player.name,
            number=player.number,
            active=player.active,
        )
        for player in result.players
    ]
