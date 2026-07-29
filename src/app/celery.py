from celery import Celery

from app.core.config import settings

celery_app = Celery("app", broker=settings.celery.broker_url)

celery_app.autodiscover_tasks(["app.tasks.file_sync"])
