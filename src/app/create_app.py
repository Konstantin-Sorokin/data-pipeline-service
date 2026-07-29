import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import router
from app.api.routers.pages import router as pages_router
from app.core.db_helper import db_helper

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управлять жизненным циклом приложения: инициализация и завершение."""
    logger.info("Application started")
    print("API LOOP", id(asyncio.get_running_loop()))

    yield

    logger.info("Shutting down")
    await db_helper.dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        lifespan=lifespan,
    )

    app.include_router(router)
    app.include_router(pages_router)

    @app.get("/health", include_in_schema=False)
    async def health():
        return {"status": "ok"}

    return app
