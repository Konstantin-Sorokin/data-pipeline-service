from typing import Annotated

from fastapi import APIRouter, Query

from app.core.config import settings
from app.dependencies.services import FileServiceDep
from app.schemas.files import PaginatedFilesResponse

router = APIRouter(prefix=settings.api.files_prefix)


@router.get("", response_model=PaginatedFilesResponse)
async def get_files(
    service: FileServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 50,
):
    return await service.get_files(
        page=page,
        page_size=page_size,
    )
