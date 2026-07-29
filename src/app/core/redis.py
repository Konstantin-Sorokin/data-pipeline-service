from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis.from_url(
    settings.redis.url,
    decode_responses=True,
)
