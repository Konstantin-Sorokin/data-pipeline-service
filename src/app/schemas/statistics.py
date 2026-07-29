from pydantic import BaseModel


class StatisticsRequest(BaseModel):
    file_ids: list[int] | None = None
    all_files: bool = False


class StatisticsResponse(BaseModel):
    statistics: dict[int, int]
