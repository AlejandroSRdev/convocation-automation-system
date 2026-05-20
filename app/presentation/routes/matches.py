from fastapi import APIRouter, Depends

from app.application.use_cases.get_matches import GetMatchesUseCase
from app.presentation.dependencies import get_get_matches_use_case
from app.presentation.schemas.match import MatchResponse

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=list[MatchResponse])
def list_matches(
    use_case: GetMatchesUseCase = Depends(get_get_matches_use_case),
) -> list[MatchResponse]:
    result = use_case.execute()
    return [
        MatchResponse(
            id=match.id,
            home_team=match.home_team,
            away_team=match.away_team,
            matchday=match.matchday,
            match_date=match.match_date,
            match_time=match.match_time,
            location=match.location,
            competition_type=match.competition_type,
        )
        for match in result.matches
    ]
