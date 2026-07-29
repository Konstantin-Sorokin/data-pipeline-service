from contextlib import asynccontextmanager
from typing import Annotated

import httpx
from fastapi import Depends

from app.clients.file_provider import FileProviderClient
from app.core.config import settings
from app.core.unit_of_work import UnitOfWork
from app.dependencies.redis import RedisDep, create_redis
from app.dependencies.storage import get_file_storage
from app.dependencies.uow import UOW_Dep
from app.services.download import DownloadService
from app.services.file import FileService
from app.services.statistics import StatisticsService


@asynccontextmanager
async def download_service_context(session):
    """Создать контекстный менеджер для сервиса загрузки файлов."""

    redis = create_redis()

    async with httpx.AsyncClient(timeout=30) as client:
        service = DownloadService(
            client=FileProviderClient(
                client=client,
                base_url=settings.file_provider.url,
                candidate_id=settings.file_provider.candidate_id,
            ),
            uow=UnitOfWork(session),
            storage=get_file_storage(),
            redis=redis,
        )

        try:
            yield service

        finally:
            await redis.close()


def get_file_service(uow: UOW_Dep) -> FileService:
    return FileService(uow)


def get_statistics_service(uow: UOW_Dep, redis: RedisDep) -> StatisticsService:
    return StatisticsService(uow=uow, redis=redis)


FileServiceDep = Annotated[FileService, Depends(get_file_service)]

StatisticsServiceDep = Annotated[StatisticsService, Depends(get_statistics_service)]
