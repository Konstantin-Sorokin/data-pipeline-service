from datetime import datetime

from pydantic import BaseModel


class FileRead(BaseModel):
    id: int
    name: str
    downloaded_at: datetime
    statistics: dict[int, int]

    model_config = {
        "from_attributes": True,
    }


class PaginatedFilesResponse(BaseModel):
    items: list[FileRead]
    total: int
    page: int
    page_size: int
