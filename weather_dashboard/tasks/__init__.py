"""
Tasks module initialization
"""
from .celery_app import celery_app
from .weather_tasks import (
    fetch_weather_for_locations,
    fetch_weather_for_default_locations,
    cleanup_old_weather_data
)

__all__ = [
    "celery_app",
    "fetch_weather_for_locations",
    "fetch_weather_for_default_locations", 
    "cleanup_old_weather_data"
]