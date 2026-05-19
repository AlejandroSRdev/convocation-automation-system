from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.refine_convocation import RefineConvocationUseCase, RefineConvocationResult
from app.presentation.schemas.convocation import RefineConvocationRequest, RefineConvocationResponse

router = APIRouter(prefix="/convocations", tags=["convocations"])


def get_refine_convocation_use_case() -> RefineConvocationUseCase:
    raise NotImplementedError("Dependency not wired")


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
