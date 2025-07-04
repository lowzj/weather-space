"""
API schemas initialization
"""
from .weather import (
    WeatherDataCreate,
    WeatherDataResponse,
    FavoriteLocationCreate,
    FavoriteLocationResponse,
    WeatherAlertCreate,
    WeatherAlertResponse,
    WeatherSummary,
    HourlyWeatherTrend,
    LocationComparison
)

__all__ = [
    "WeatherDataCreate",
    "WeatherDataResponse", 
    "FavoriteLocationCreate",
    "FavoriteLocationResponse",
    "WeatherAlertCreate",
    "WeatherAlertResponse",
    "WeatherSummary",
    "HourlyWeatherTrend",
    "LocationComparison"
]