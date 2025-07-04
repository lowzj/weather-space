"""
Weather data schemas for API validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class WeatherDataBase(BaseModel):
    """Base weather data schema"""
    location_name: str
    latitude: Decimal
    longitude: Decimal
    temperature: Optional[Decimal] = None
    feels_like: Optional[Decimal] = None
    humidity: Optional[int] = None
    pressure: Optional[Decimal] = None
    visibility: Optional[Decimal] = None
    uv_index: Optional[Decimal] = None
    wind_speed: Optional[Decimal] = None
    wind_direction: Optional[int] = None
    weather_condition: Optional[str] = None
    weather_description: Optional[str] = None
    cloud_coverage: Optional[int] = None
    api_source: str = "openweathermap"


class WeatherDataCreate(WeatherDataBase):
    """Schema for creating weather data"""
    pass


class WeatherDataResponse(WeatherDataBase):
    """Schema for weather data response"""
    id: int
    recorded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class FavoriteLocationBase(BaseModel):
    """Base favorite location schema"""
    location_name: str
    latitude: Decimal
    longitude: Decimal
    is_default: bool = False


class FavoriteLocationCreate(FavoriteLocationBase):
    """Schema for creating favorite location"""
    user_id: str = "lowzj"


class FavoriteLocationResponse(FavoriteLocationBase):
    """Schema for favorite location response"""
    id: int
    user_id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class WeatherAlertBase(BaseModel):
    """Base weather alert schema"""
    location_name: str
    alert_type: str
    severity: str
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class WeatherAlertCreate(WeatherAlertBase):
    """Schema for creating weather alert"""
    pass


class WeatherAlertResponse(WeatherAlertBase):
    """Schema for weather alert response"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class WeatherSummary(BaseModel):
    """Weather summary schema for analytics"""
    date: str
    avg_temp: Optional[Decimal]
    min_temp: Optional[Decimal]
    max_temp: Optional[Decimal]
    avg_humidity: Optional[Decimal]
    avg_wind_speed: Optional[Decimal]
    dominant_condition: Optional[str]


class HourlyWeatherTrend(BaseModel):
    """Hourly weather trend schema"""
    hour: datetime
    avg_temp: Optional[Decimal]
    min_temp: Optional[Decimal]
    max_temp: Optional[Decimal]
    avg_humidity: Optional[Decimal]


class LocationComparison(BaseModel):
    """Multi-location comparison schema"""
    location_name: str
    temperature: Optional[Decimal]
    humidity: Optional[int]
    weather_condition: Optional[str]
    wind_speed: Optional[Decimal]
    recorded_at: datetime