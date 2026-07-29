from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.core.config import BASE_DIR, settings
from app.dependencies.clients import FileProviderClientDep
from app.dependencies.redis import RedisDep
from app.utils.redis_keys import CacheKey

router = APIRouter()

templates = Jinja2Templates(directory=BASE_DIR / "src" / "app" / "templates")


@router.get("/files")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="files.html",
    )


@router.get("/download")
async def download_page(
    request: Request,
    redis: RedisDep,
    file_provider: FileProviderClientDep,
):
    """Отобразить страницу загрузки с информацией о статусе синхронизации."""

    key = CacheKey.file_sync(settings.file_provider.candidate_id)

    sync_status = await redis.hgetall(key)

    status = sync_status.get("status")

    context = {
        "status": status,
        "has_files": False,
    }

    if not status:
        names = await file_provider.get_names()

        context["has_files"] = bool(names)

    return templates.TemplateResponse(
        request=request,
        name="download.html",
        context=context,
    )
