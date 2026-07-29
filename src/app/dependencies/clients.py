from typing import Annotated

import httpx
from fastapi import Depends

from app.clients.file_provider import FileProviderClient
from app.core.config import settings


def get_file_provider_client() -> FileProviderClient:
    """Создать клиент для взаимодействия с файловым провайдером."""
    client = httpx.AsyncClient()

    return FileProviderClient(
        client=client,
        base_url=settings.file_provider.url,
        candidate_id=settings.file_provider.candidate_id,
    )


FileProviderClientDep = Annotated[
    FileProviderClient,
    Depends(get_file_provider_client),
]
