from pydantic import BaseModel


class DownloadRequest(BaseModel):
    file_names: list[str]


class FileNamesResponse(BaseModel):
    file_names: list[str]


class MarkDownloadedRequest(BaseModel):
    file_names: list[str]
