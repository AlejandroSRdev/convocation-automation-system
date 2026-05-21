from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.refine_convocation import RefineConvocationUseCase, RefineConvocationResult
from app.application.use_cases.generate_convocation import (
    GenerateConvocationUseCase,
    GenerateConvocationCommand,
    InvitedPlayerInput as InvitedPlayerCommandInput,
)
from app.domain.exceptions import MatchNotFoundError
from app.presentation.dependencies import get_generate_convocation_use_case, get_refine_convocation_use_case
from app.presentation.schemas.convocation import (
    RefineConvocationRequest,
    RefineConvocationResponse,
    GenerateConvocationRequest,
    GenerateConvocationResponse,
    MatchInfo,
    PlayerInfo,
    StaffInfo,
)

router = APIRouter(prefix="/convocations", tags=["convocations"])


@router.post("/refine", response_model=RefineConvocationResponse)
def refine_convocation(
    request: RefineConvocationRequest,
    use_case: RefineConvocationUseCase = Depends(get_refine_convocation_use_case),
) -> RefineConvocationResponse:
    try:
        result = use_case.execute(
            message=request.message,
            critical_fragments=request.critical_fragments,
            style=request.style,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    return RefineConvocationResponse(
        refined_message=result.message,
        was_refined=result.was_refined,
    )


@router.post("/generate", response_model=GenerateConvocationResponse)
def generate_convocation(
    request: GenerateConvocationRequest,
    use_case: GenerateConvocationUseCase = Depends(get_generate_convocation_use_case),
) -> GenerateConvocationResponse:
    command = GenerateConvocationCommand(
        match_id=request.match_id,
        convocation_time=request.convocation_time,
        selected_staff_ids=request.selected_staff_ids,
        player_innings={int(k): v for k, v in request.player_innings.items()},
        excluded_player_ids=request.excluded_player_ids,
        invited_players=[
            InvitedPlayerCommandInput(name=p.name, number=p.number)
            for p in request.invited_players
        ],
        manual_notes=request.manual_notes,
    )
    try:
        result = use_case.execute(command)
    except MatchNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return GenerateConvocationResponse(
        rendered_message=result.rendered_message,
        match_metadata=MatchInfo(
            home_team=result.home_team,
            away_team=result.away_team,
            matchday=result.matchday,
            match_date=result.match_date.isoformat(),
            match_time=result.match_time.strftime("%H:%M"),
            location=result.location,
            competition_type=result.competition_type,
        ),
        selected_players=[
            PlayerInfo(
                number=p.number,
                name=p.name,
                innings=p.innings,
                category_badge=p.category_badge,
            )
            for p in result.selected_players
        ],
        selected_staff=[
            StaffInfo(role=s.role, name=s.name)
            for s in result.selected_staff
        ],
        critical_fragments=result.critical_fragments,
    )
