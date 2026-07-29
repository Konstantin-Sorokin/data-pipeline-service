import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]
STORAGE_PATH = BASE_DIR / "storage"


LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"

    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class ApiConfig(BaseModel):
    prefix: str = "/api"

    sync_prefix: str = "/sync"
    files_prefix: str = "/files"
    statistics_prefix: str = "/statistics"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False


class DatabaseConfig(BaseModel):
    url: PostgresDsn

    echo: bool = False
    echo_pool: bool = False

    pool_size: int = 5
    max_overflow: int = 10


class RedisConfig(BaseModel):
    url: str


class CeleryConfig(BaseModel):
    broker_url: str


class FileProvider(BaseModel):
    url: str
    candidate_id: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )

    run: RunConfig = RunConfig()
    api: ApiConfig = ApiConfig()
    logging: LoggingConfig = LoggingConfig()
    db: DatabaseConfig
    redis: RedisConfig
    celery: CeleryConfig
    file_provider: FileProvider


settings = Settings()
