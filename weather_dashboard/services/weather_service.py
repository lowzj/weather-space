"""
Weather service for data management and analytics
"""
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from weather_dashboard.models.weather import WeatherData, FavoriteLocation, WeatherAlert
from weather_dashboard.schemas.weather import (
    WeatherDataCreate, WeatherSummary, HourlyWeatherTrend, LocationComparison
)
from weather_dashboard.services.openweather import OpenWeatherMapService

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for weather data management and analytics"""
    
    def __init__(self, db: Session):
        self.db = db
        self.openweather = OpenWeatherMapService()
    
    def fetch_and_store_weather(self, locations: List[str]) -> Dict[str, bool]:
        """
        Fetch weather data from API and store in database
        
        Args:
            locations: List of location strings
            
        Returns:
            Dictionary with location as key and success status as value
        """
        results = {}
        
        for location in locations:
            try:
                weather_data = self.openweather.get_current_weather(location)
                if weather_data:
                    self.create_weather_data(WeatherDataCreate(**weather_data))
                    results[location] = True
                    logger.info(f"Successfully stored weather data for {location}")
                else:
                    results[location] = False
                    logger.error(f"Failed to fetch weather data for {location}")
            except Exception as e:
                results[location] = False
                logger.error(f"Error processing weather data for {location}: {e}")
        
        return results
    
    def create_weather_data(self, weather_data: WeatherDataCreate) -> WeatherData:
        """Create new weather data record"""
        db_weather = WeatherData(**weather_data.model_dump())
        self.db.add(db_weather)
        self.db.commit()
        self.db.refresh(db_weather)
        return db_weather
    
    def get_current_weather_overview(self) -> Optional[WeatherData]:
        """Get current weather overview (most recent within 1 hour)"""
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        return (
            self.db.query(WeatherData)
            .filter(WeatherData.recorded_at >= cutoff_time)
            .order_by(desc(WeatherData.recorded_at))
            .first()
        )
    
    def get_hourly_temperature_trend(self, hours: int = 24) -> List[HourlyWeatherTrend]:
        """Get hourly temperature trend for last N hours"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = text("""
            SELECT 
                DATE_TRUNC('hour', recorded_at) as hour,
                AVG(temperature) as avg_temp,
                MIN(temperature) as min_temp,
                MAX(temperature) as max_temp,
                AVG(humidity) as avg_humidity
            FROM weather_data 
            WHERE recorded_at >= :cutoff_time
            GROUP BY DATE_TRUNC('hour', recorded_at)
            ORDER BY hour
        """)
        
        result = self.db.execute(query, {'cutoff_time': cutoff_time})
        return [
            HourlyWeatherTrend(
                hour=row.hour,
                avg_temp=row.avg_temp,
                min_temp=row.min_temp,
                max_temp=row.max_temp,
                avg_humidity=row.avg_humidity
            )
            for row in result
        ]
    
    def get_weekly_weather_summary(self, days: int = 7) -> List[WeatherSummary]:
        """Get weekly weather summary for last N days"""
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        
        query = text("""
            SELECT 
                DATE(recorded_at) as date,
                AVG(temperature) as avg_temp,
                MIN(temperature) as min_temp,
                MAX(temperature) as max_temp,
                AVG(humidity) as avg_humidity,
                AVG(wind_speed) as avg_wind_speed,
                MODE() WITHIN GROUP (ORDER BY weather_condition) as dominant_condition
            FROM weather_data 
            WHERE recorded_at >= :cutoff_time
            GROUP BY DATE(recorded_at)
            ORDER BY date
        """)
        
        result = self.db.execute(query, {'cutoff_time': cutoff_time})
        return [
            WeatherSummary(
                date=str(row.date),
                avg_temp=row.avg_temp,
                min_temp=row.min_temp,
                max_temp=row.max_temp,
                avg_humidity=row.avg_humidity,
                avg_wind_speed=row.avg_wind_speed,
                dominant_condition=row.dominant_condition
            )
            for row in result
        ]
    
    def get_multi_location_comparison(self, hours: int = 2) -> List[LocationComparison]:
        """Get multi-location comparison for latest readings"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = text("""
            WITH latest_readings AS (
                SELECT DISTINCT ON (location_name) 
                    location_name,
                    temperature,
                    humidity,
                    weather_condition,
                    wind_speed,
                    recorded_at
                FROM weather_data 
                WHERE recorded_at >= :cutoff_time
                ORDER BY location_name, recorded_at DESC
            )
            SELECT * FROM latest_readings
            ORDER BY temperature DESC
        """)
        
        result = self.db.execute(query, {'cutoff_time': cutoff_time})
        return [
            LocationComparison(
                location_name=row.location_name,
                temperature=row.temperature,
                humidity=row.humidity,
                weather_condition=row.weather_condition,
                wind_speed=row.wind_speed,
                recorded_at=row.recorded_at
            )
            for row in result
        ]
    
    def get_weather_history(self, location: str, days: int = 30) -> List[WeatherData]:
        """Get weather history for a specific location"""
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        return (
            self.db.query(WeatherData)
            .filter(
                WeatherData.location_name == location,
                WeatherData.recorded_at >= cutoff_time
            )
            .order_by(desc(WeatherData.recorded_at))
            .all()
        )