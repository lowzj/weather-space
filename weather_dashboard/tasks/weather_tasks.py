"""
Weather data collection tasks
"""
import logging
from typing import List
from celery import Task
from weather_dashboard.tasks.celery_app import celery_app
from weather_dashboard.core.config import settings
from weather_dashboard.core.database import SessionLocal
from weather_dashboard.services.weather_service import WeatherService

logger = logging.getLogger(__name__)


class DatabaseTask(Task):
    """Base task with database session handling"""
    
    def __call__(self, *args, **kwargs):
        with SessionLocal() as db:
            try:
                return super().__call__(db, *args, **kwargs)
            except Exception as e:
                logger.error(f"Task failed: {e}")
                db.rollback()
                raise
            finally:
                db.close()


@celery_app.task(base=DatabaseTask, bind=True)
def fetch_weather_for_locations(self, db, locations: List[str]):
    """
    Fetch weather data for specified locations
    
    Args:
        db: Database session
        locations: List of location strings
    """
    logger.info(f"Starting weather data fetch for {len(locations)} locations")
    
    try:
        weather_service = WeatherService(db)
        results = weather_service.fetch_and_store_weather(locations)
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        logger.info(f"Weather data fetch completed: {success_count}/{total_count} successful")
        
        return {
            "success": True,
            "message": f"Fetched weather data for {success_count}/{total_count} locations",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in weather data fetch task: {e}")
        return {
            "success": False,
            "message": f"Failed to fetch weather data: {str(e)}"
        }


@celery_app.task
def fetch_weather_for_default_locations():
    """
    Fetch weather data for default locations
    """
    logger.info("Starting periodic weather data fetch for default locations")
    
    try:
        locations = settings.default_locations
        result = fetch_weather_for_locations.delay(locations)
        
        logger.info(f"Queued weather data fetch task for {len(locations)} default locations")
        
        return {
            "success": True,
            "message": f"Queued weather data fetch for {len(locations)} default locations",
            "task_id": result.id
        }
    except Exception as e:
        logger.error(f"Error queuing weather data fetch task: {e}")
        return {
            "success": False,
            "message": f"Failed to queue weather data fetch: {str(e)}"
        }


@celery_app.task(base=DatabaseTask, bind=True)
def cleanup_old_weather_data(self, db, days: int = 90):
    """
    Clean up weather data older than specified days
    
    Args:
        db: Database session
        days: Number of days to keep (default: 90)
    """
    from datetime import datetime, timedelta
    from weather_dashboard.models.weather import WeatherData
    
    logger.info(f"Starting cleanup of weather data older than {days} days")
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        deleted_count = (
            db.query(WeatherData)
            .filter(WeatherData.recorded_at < cutoff_date)
            .delete()
        )
        
        db.commit()
        
        logger.info(f"Cleanup completed: {deleted_count} records deleted")
        
        return {
            "success": True,
            "message": f"Cleaned up {deleted_count} old weather records",
            "deleted_count": deleted_count
        }
    except Exception as e:
        logger.error(f"Error in cleanup task: {e}")
        db.rollback()
        return {
            "success": False,
            "message": f"Failed to cleanup old data: {str(e)}"
        }