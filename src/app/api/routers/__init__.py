from fastapi import APIRouter

from app.api.routers.files import router as files_router
from app.api.routers.statistics import router as statistics_router
from app.api.routers.sync import router as sync_router
from app.core.config import settings

router = APIRouter(prefix=settings.api.prefix)

router.include_router(sync_router)
router.include_router(files_router)
router.include_router(statistics_router)
