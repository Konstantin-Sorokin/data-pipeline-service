import asyncio

import httpx

from app.clients.base import BaseApiClient
from app.clients.exceptions import (
    FileProviderBlockedError,
    FileProviderRateLimitError,
)
from app.schemas.external.file_provider import FileNamesResponse


class FileProviderClient(BaseApiClient):
    REQUEST_DELAY = 0.8

    def __init__(self, client: httpx.AsyncClient, base_url: str, candidate_id: str):
        super().__init__(client, base_url)
        self._candidate_id = candidate_id

    async def get_names(self) -> list[str]:
        """Получить список имён файлов от провайдера."""
        await self._wait()
        response = await self.get(
            "/api/files/names",
            headers={"x-candidate-id": self._candidate_id},
        )

        response = self._handle_response(response)

        return FileNamesResponse.model_validate(response.json()).file_names

    async def download(self, file_names: list[str]) -> bytes:
        """Скачать архив с файлами по именам."""
        await self._wait()
        response = await self.post(
            "/api/files/download",
            json={"file_names": file_names},
        )

        response = self._handle_response(response)

        return response.content

    async def mark_downloaded(self, file_names: list[str]) -> None:
        """Отметить файлы как скачанные у провайдера."""
        await self._wait()
        response = await self.post(
            "/api/files/downloaded",
            headers={"x-candidate-id": self._candidate_id},
            json={"file_names": file_names},
        )

        self._handle_response(response)

    async def _wait(self):
        """Выдержать паузу между запросами для соблюдения rate limit."""
        await asyncio.sleep(self.REQUEST_DELAY)

    @staticmethod
    def _handle_response(response: httpx.Response) -> httpx.Response:
        """Обработать ответ API и выбросить исключение при ошибке."""

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")

            raise FileProviderRateLimitError(
                retry_after=int(retry_after) if retry_after else None
            )

        if response.status_code == 403:
            retry_after = response.headers.get("Retry-After")

            raise FileProviderBlockedError(
                retry_after=int(retry_after) if retry_after else None,
            )

        response.raise_for_status()

        return response
