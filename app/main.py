from fastapi import FastAPI

from app.config.logging import configure_logging
from app.config.settings import settings
from app.infrastructure.ai.openai_adapter import OpenAIAdapter
from app.application.use_cases.refine_convocation import RefineConvocationUseCase
from app.presentation.routes.health import router as health_router
from app.presentation.routes import convocations as convocations_module
from app.presentation.routes.convocations import router as convocations_router

configure_logging()

app = FastAPI(title=settings.APP_NAME)


def get_refine_convocation_use_case() -> RefineConvocationUseCase:
    adapter = OpenAIAdapter(api_key=settings.OPENAI_API_KEY)
    return RefineConvocationUseCase(provider=adapter)


convocations_module.get_refine_convocation_use_case = get_refine_convocation_use_case

app.include_router(health_router)
app.include_router(convocations_router)
