from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.infrastructure.ai.openai_adapter import OpenAIAdapter
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.repositories.match_repository import SQLMatchRepository
from app.infrastructure.database.repositories.player_repository import SQLPlayerRepository
from app.infrastructure.database.repositories.staff_repository import SQLStaffRepository
from app.application.rendering.convocation_renderer import ConvocationRenderer
from app.application.use_cases.generate_convocation import GenerateConvocationUseCase
from app.application.use_cases.get_matches import GetMatchesUseCase
from app.application.use_cases.refine_convocation import RefineConvocationUseCase


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_generate_convocation_use_case(
    db: Session = Depends(get_db),
) -> GenerateConvocationUseCase:
    return GenerateConvocationUseCase(
        match_repository=SQLMatchRepository(db),
        player_repository=SQLPlayerRepository(db),
        staff_repository=SQLStaffRepository(db),
        renderer=ConvocationRenderer(),
    )


def get_get_matches_use_case(
    db: Session = Depends(get_db),
) -> GetMatchesUseCase:
    return GetMatchesUseCase(
        match_repository=SQLMatchRepository(db),
    )


def get_refine_convocation_use_case() -> RefineConvocationUseCase:
    adapter = OpenAIAdapter(api_key=settings.OPENAI_API_KEY)
    return RefineConvocationUseCase(provider=adapter)
