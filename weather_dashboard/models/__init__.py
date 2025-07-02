"""
Database models initialization
"""
from .weather import WeatherData, FavoriteLocation, WeatherAlert

__all__ = ["WeatherData", "FavoriteLocation", "WeatherAlert"]