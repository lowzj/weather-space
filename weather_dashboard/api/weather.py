"""
Weather API endpoints
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from weather_dashboard.core.database import get_db
from weather_dashboard.schemas.weather import (
    WeatherDataResponse,
    WeatherSummary,
    HourlyWeatherTrend,
    LocationComparison
)
from weather_dashboard.services.weather_service import WeatherService
from weather_dashboard.models.weather import WeatherAlert

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current", response_model=Optional[WeatherDataResponse])
async def get_current_weather(db: Session = Depends(get_db)):
    """Get current weather overview"""
    try:
        weather_service = WeatherService(db)
        current_weather = weather_service.get_current_weather_overview()
        
        if not current_weather:
            raise HTTPException(status_code=404, detail="No recent weather data found")
        
        return current_weather
    except Exception as e:
        logger.error(f"Error getting current weather: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/trends/hourly", response_model=List[HourlyWeatherTrend])
async def get_hourly_trends(
    hours: int = Query(24, ge=1, le=168, description="Number of hours (1-168)"),
    db: Session = Depends(get_db)
):
    """Get hourly temperature trends"""
    try:
        weather_service = WeatherService(db)
        trends = weather_service.get_hourly_temperature_trend(hours)
        return trends
    except Exception as e:
        logger.error(f"Error getting hourly trends: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/summary/weekly", response_model=List[WeatherSummary])
async def get_weekly_summary(
    days: int = Query(7, ge=1, le=30, description="Number of days (1-30)"),
    db: Session = Depends(get_db)
):
    """Get weekly weather summary"""
    try:
        weather_service = WeatherService(db)
        summary = weather_service.get_weekly_weather_summary(days)
        return summary
    except Exception as e:
        logger.error(f"Error getting weekly summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/comparison/locations", response_model=List[LocationComparison])
async def get_location_comparison(
    hours: int = Query(2, ge=1, le=24, description="Hours to look back (1-24)"),
    db: Session = Depends(get_db)
):
    """Get multi-location comparison"""
    try:
        weather_service = WeatherService(db)
        comparison = weather_service.get_multi_location_comparison(hours)
        return comparison
    except Exception as e:
        logger.error(f"Error getting location comparison: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history/{location}")
async def get_weather_history(
    location: str,
    days: int = Query(30, ge=1, le=365, description="Number of days (1-365)"),
    db: Session = Depends(get_db)
):
    """Get weather history for a specific location"""
    try:
        weather_service = WeatherService(db)
        history = weather_service.get_weather_history(location, days)
        return history
    except Exception as e:
        logger.error(f"Error getting weather history for {location}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/fetch")
async def fetch_weather_data(
    locations: List[str] = Query(description="List of locations to fetch weather data for"),
    db: Session = Depends(get_db)
):
    """Manually trigger weather data fetching for specified locations"""
    try:
        weather_service = WeatherService(db)
        results = weather_service.fetch_and_store_weather(locations)
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        return {
            "message": f"Fetched weather data for {success_count}/{total_count} locations",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/alerts")
async def get_active_alerts(db: Session = Depends(get_db)):
    """Get active weather alerts"""
    try:
        from datetime import datetime
        from sqlalchemy import or_
        
        active_alerts = (
            db.query(WeatherAlert)
            .filter(
                or_(
                    WeatherAlert.end_time > datetime.utcnow(),
                    WeatherAlert.end_time.is_(None)
                )
            )
            .order_by(
                WeatherAlert.severity.desc(),
                WeatherAlert.start_time.desc()
            )
            .all()
        )
        
        return active_alerts
    except Exception as e:
        logger.error(f"Error getting active alerts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")