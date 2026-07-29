from datetime import datetime, timezone
from io import BytesIO
from zipfile import ZipFile

from redis.asyncio import Redis

from app.clients.file_provider import FileProviderClient
from app.core.config import settings
from app.core.unit_of_work import UnitOfWork
from app.storage.file_storage import FileStorage
from app.utils.calculate_digit_statistics import calculate_digit_statistics
from app.utils.redis_keys import CacheKey


class DownloadService:
    def __init__(
        self,
        client: FileProviderClient,
        uow: UnitOfWork,
        storage: FileStorage,
        redis: Redis,
    ):
        self.client = client
        self.uow = uow
        self.storage = storage
        self.redis = redis

    async def sync_files(self) -> None:
        """Синхронизировать файлы с внешним провайдером."""
        names = await self.client.get_names()
        key = CacheKey.file_sync(settings.file_provider.candidate_id)
        if not names:
            await self.redis.hset(
                key,
                mapping={
                    "status": "completed",
                },
            )
            return
        await self.redis.hset(
            key,
            mapping={
                "status": "running",
            },
        )
        try:
            while True:
                names = await self.client.get_names()

                if not names:
                    break

                new_names = await self._get_new_names(names)

                await self.redis.hincrby(key, "total", len(new_names))

                while new_names:
                    batch = new_names[:3]

                    files, downloaded_at = await self._download_and_extract_batch(batch)

                    for name, content in files:
                        await self._process_file(
                            name=name,
                            content=content,
                            downloaded_at=downloaded_at,
                        )
                    await self.client.mark_downloaded(batch)

                    del new_names[:3]

            await self.redis.hset(
                key,
                mapping={"status": "completed"},
            )

        except Exception:
            await self.redis.hset(
                key,
                mapping={"status": "failed"},
            )
            raise

    async def _get_new_names(self, names: list[str]) -> list[str]:
        """Отфильтровать имена файлов, которых ещё нет в базе."""
        existing_names = await self.uow.files.get_existing_names(names)

        return [name for name in names if name not in existing_names]

    async def _download_and_extract_batch(
        self,
        names: list[str],
    ) -> tuple[list[tuple[str, bytes]], datetime]:
        """Скачать и распаковать архив с файлами."""
        archive = await self.client.download(names)
        downloaded_at = datetime.now(timezone.utc)
        files = self._extract_zip(archive)

        return files, downloaded_at

    async def _process_file(
        self, name: str, content: bytes, downloaded_at: datetime
    ) -> None:
        """Сохранить файл, рассчитать статистику и записать в БД."""
        key = CacheKey.file_sync(settings.file_provider.candidate_id)
        file_path = await self.storage.save(
            name=name,
            content=content,
        )

        calculation = calculate_digit_statistics(content)

        async with self.uow:
            db_file = await self.uow.files.create(
                name=name,
                path=file_path,
                downloaded_at=downloaded_at,
            )

            await self.uow.calculations.create(
                file_id=db_file.id,
                counts=calculation,
            )

        await self.redis.hincrby(
            key,
            "downloaded",
            1,
        )

    @staticmethod
    def _extract_zip(archive: bytes) -> list[tuple[str, bytes]]:
        """Извлечь файлы из zip-архива."""
        files = []

        with ZipFile(BytesIO(archive)) as zip_file:
            for name in zip_file.namelist():
                content = zip_file.read(name)

                files.append((name, content))

        return files
