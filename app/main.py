from fastapi import FastAPI

from app.config.logging import configure_logging
from app.config.settings import settings
from app.presentation.routes.health import router as health_router

configure_logging()

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
