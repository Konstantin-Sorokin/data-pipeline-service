from datetime import datetime

from sqlalchemy import exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import File


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        name: str,
        path: str,
        downloaded_at: datetime,
    ) -> File:
        """Создать запись о файле в базе данных."""
        file = File(
            name=name,
            path=path,
            downloaded_at=downloaded_at,
        )

        self.session.add(file)
        await self.session.flush()

        return file

    async def get_existing_names(
        self,
        names: list[str],
    ) -> set[str]:
        """Получить имена файлов, уже сохранённых в базе."""
        stmt = select(File.name).where(File.name.in_(names))

        result = await self.session.scalars(stmt)

        return set(result.all())

    async def get_paginated(
        self,
        limit: int,
        offset: int,
    ) -> list[File]:
        """Получить список файлов с пагинацией."""
        stmt = (
            select(File)
            .options(selectinload(File.calculation))
            .order_by(
                File.downloaded_at.asc(),
                File.id.asc(),
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.scalars(stmt)

        return list(result)

    async def count(self) -> int:
        """Получить общее количество файлов."""
        stmt = select(func.count()).select_from(File)

        result = await self.session.scalar(stmt)

        return result or 0
