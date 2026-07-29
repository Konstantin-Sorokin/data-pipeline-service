from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Calculation


class CalculationRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(
        self,
        file_id: int,
        counts: dict[int, int],
    ) -> Calculation:
        """Создать запись статистики по цифрам для файла."""
        calculation = Calculation(
            file_id=file_id,
            digit_0_count=counts[0],
            digit_1_count=counts[1],
            digit_2_count=counts[2],
            digit_3_count=counts[3],
            digit_4_count=counts[4],
            digit_5_count=counts[5],
            digit_6_count=counts[6],
            digit_7_count=counts[7],
            digit_8_count=counts[8],
            digit_9_count=counts[9],
        )

        self.session.add(calculation)

        await self.session.flush()

        return calculation

    async def get_by_file_ids(
        self,
        file_ids: list[int],
    ) -> list[Calculation]:
        """Получить расчёты для указанных файлов."""
        stmt = select(Calculation).where(Calculation.file_id.in_(file_ids))

        result = await self.session.scalars(stmt)

        return list(result)

    async def get_all(self) -> list[Calculation]:
        """Получить все расчёты."""
        stmt = select(Calculation)

        result = await self.session.scalars(stmt)

        return list(result)
