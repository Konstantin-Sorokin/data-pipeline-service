from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings
from app.dependencies.redis import RedisDep
from app.tasks.file_sync import sync_files_task
from app.utils.redis_keys import CacheKey

router = APIRouter(prefix=settings.api.sync_prefix)


@router.post("")
async def start_sync(redis: RedisDep):
    """Запустить синхронизацию файлов с внешним провайдером."""
    key = CacheKey.file_sync(settings.file_provider.candidate_id)
    await redis.hset(
        key,
        mapping={
            "status": "queued",
            "total": 0,
            "downloaded": 0,
            "started_at": datetime.now(timezone.utc).isoformat(),
        },
    )

    sync_files_task.delay()

    return {"status": "started"}


@router.get("")
async def get_sync_status(redis: RedisDep):
    """Получить текущий статус синхронизации."""
    key = CacheKey.file_sync(settings.file_provider.candidate_id)

    data = await redis.hgetall(key)

    return {
        k.decode() if isinstance(k, bytes) else k: v.decode()
        if isinstance(v, bytes)
        else v
        for k, v in data.items()
    }
