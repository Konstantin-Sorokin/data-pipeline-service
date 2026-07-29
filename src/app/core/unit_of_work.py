from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.calculation import CalculationRepository
from app.repositories.file import FileRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.calculations = CalculationRepository(session)
        self.files = FileRepository(session)

    async def commit(self) -> None:
        """Зафиксировать транзакцию."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Откатить транзакцию."""
        await self.session.rollback()

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Зафиксировать или откатить транзакцию при выходе из контекстного менеджера."""
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self.session.close()
