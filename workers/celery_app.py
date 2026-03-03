from celery import Celery
from core.config import REDIS_URL

celery_app = Celery(
    "ielts_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,           # job results live in Redis for 1 hour
    worker_prefetch_multiplier=1,  # one task at a time per worker (IO-bound)
)
