"""
Celery application configuration
"""
import logging
from celery import Celery
from weather_dashboard.core.config import settings

logger = logging.getLogger(__name__)

# Create Celery app
celery_app = Celery(
    "weather_dashboard",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["weather_dashboard.tasks.weather_tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    "fetch-weather-data": {
        "task": "weather_dashboard.tasks.weather_tasks.fetch_weather_for_default_locations",
        "schedule": settings.fetch_interval_minutes * 60.0,  # Convert minutes to seconds
    },
}

if __name__ == "__main__":
    celery_app.start()