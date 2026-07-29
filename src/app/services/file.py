from app.core.unit_of_work import UnitOfWork
from app.schemas.files import FileRead, PaginatedFilesResponse


class FileService:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.uow = uow

    async def get_files(
        self,
        page: int,
        page_size: int,
    ) -> PaginatedFilesResponse:
        """Получить список файлов с пагинацией и статистикой по цифрам."""
        offset = (page - 1) * page_size

        files = await self.uow.files.get_paginated(
            limit=page_size,
            offset=offset,
        )

        total = await self.uow.files.count()

        items = []

        for file in files:
            items.append(
                FileRead(
                    id=file.id,
                    name=file.name,
                    downloaded_at=file.downloaded_at,
                    statistics={
                        digit: getattr(
                            file.calculation,
                            f"digit_{digit}_count",
                        )
                        for digit in range(10)
                    },
                )
            )

        return PaginatedFilesResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )
