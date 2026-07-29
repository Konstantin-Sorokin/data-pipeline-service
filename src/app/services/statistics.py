import json
from collections import defaultdict

from fastapi import HTTPException
from redis.asyncio import Redis

from app.core.unit_of_work import UnitOfWork


class StatisticsService:
    def __init__(
        self,
        uow: UnitOfWork,
        redis: Redis,
    ):
        self.uow = uow
        self.redis = redis

    async def get_statistics(
        self,
        file_ids: list[int] | None,
        all_files: bool,
    ):
        """Получить статистику по цифрам для указанных файлов или для всех."""
        if all_files:
            return await self.get_all_statistics()

        if not file_ids:
            raise HTTPException(
                status_code=400,
                detail="No files selected",
            )

        return await self.get_statistics_summary(file_ids)

    async def get_all_statistics(self) -> dict[int, int]:
        """Получить суммарную статистику по всем файлам с кешированием."""
        cached = await self.redis.get("statistics:all")

        if cached:
            return json.loads(cached)

        calculations = await self.uow.calculations.get_all()

        total = defaultdict(int)

        for calculation in calculations:
            for digit in range(10):
                total[digit] += getattr(
                    calculation,
                    f"digit_{digit}_count",
                )

        statistics = dict(total)

        await self.redis.set(
            "statistics:all",
            json.dumps(statistics),
        )

        return statistics

    async def get_statistics_summary(
        self,
        file_ids: list[int],
    ) -> dict[int, int]:
        """Получить суммарную статистику по выбранным файлам."""
        calculations = await self.uow.calculations.get_by_file_ids(file_ids)

        total = defaultdict(int)

        for calculation in calculations:
            for digit in range(10):
                total[digit] += getattr(
                    calculation,
                    f"digit_{digit}_count",
                )

        return dict(total)
