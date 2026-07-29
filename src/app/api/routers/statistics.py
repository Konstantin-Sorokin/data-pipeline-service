from fastapi import APIRouter

from app.core.config import settings
from app.dependencies.services import StatisticsServiceDep
from app.schemas.statistics import StatisticsRequest, StatisticsResponse

router = APIRouter(prefix=settings.api.statistics_prefix)


@router.post("", response_model=StatisticsResponse)
async def get_statistics(
    data: StatisticsRequest,
    service: StatisticsServiceDep,
):
    statistics = await service.get_statistics(
        file_ids=data.file_ids,
        all_files=data.all_files,
    )

    return StatisticsResponse(
        statistics=statistics,
    )
