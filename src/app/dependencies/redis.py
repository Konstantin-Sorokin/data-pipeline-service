from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from app.core.config import settings
from app.core.redis import redis_client


def get_redis() -> Redis:
    return redis_client


def create_redis() -> Redis:
    return Redis.from_url(
        settings.redis.url,
        decode_responses=True,
    )


RedisDep = Annotated[Redis, Depends(get_redis)]
