import asyncio

from app.celery import celery_app
from app.clients.exceptions import FileProviderBlockedError, FileProviderRateLimitError
from app.core.config import settings
from app.core.db_helper import DatabaseHelper
from app.dependencies.services import download_service_context


@celery_app.task(bind=True, max_retries=5)
def sync_files_task(self):
    asyncio.run(run_sync(self))


async def run_sync(task):
    """Запустить синхронизацию файлов с обработкой ошибок и повторными попытками."""
    db_helper = DatabaseHelper(settings.db.url)

    async with db_helper.session_factory() as session:
        async with download_service_context(session=session) as service:
            try:
                await service.sync_files()

            except (
                FileProviderRateLimitError,
                FileProviderBlockedError,
            ) as exc:
                raise task.retry(
                    exc=exc,
                    countdown=(exc.retry_after or 60) + 1,
                )
