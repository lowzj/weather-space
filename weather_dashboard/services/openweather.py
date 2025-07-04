"""
OpenWeatherMap API integration service
"""
import logging
import requests
from typing import Dict, Any, Optional
from weather_dashboard.core.config import settings

logger = logging.getLogger(__name__)


class OpenWeatherMapService:
    """Service for interacting with OpenWeatherMap API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openweather_api_key
        self.base_url = settings.openweather_base_url
        
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key is required")
    
    def get_current_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data for a location
        
        Args:
            location: Location name (e.g., "New York,US" or "London,GB")
            
        Returns:
            Weather data dictionary or None if error
        """
        url = f"{self.base_url}/weather"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched weather data for {location}")
            
            return self._normalize_weather_data(data, location)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data for {location}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing weather data for {location}: {e}")
            return None
    
    def get_weather_by_coordinates(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data by coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Weather data dictionary or None if error
        """
        url = f"{self.base_url}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            location_name = f"{data.get('name', 'Unknown')},{data.get('sys', {}).get('country', 'Unknown')}"
            logger.info(f"Successfully fetched weather data for coordinates {lat},{lon}")
            
            return self._normalize_weather_data(data, location_name)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data for coordinates {lat},{lon}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing weather data for coordinates {lat},{lon}: {e}")
            return None
    
    def _normalize_weather_data(self, data: Dict[str, Any], location_name: str) -> Dict[str, Any]:
        """
        Normalize OpenWeatherMap response to our schema
        
        Args:
            data: Raw API response
            location_name: Location name
            
        Returns:
            Normalized weather data
        """
        try:
            main = data.get('main', {})
            weather = data.get('weather', [{}])[0]
            wind = data.get('wind', {})
            clouds = data.get('clouds', {})
            coord = data.get('coord', {})
            
            return {
                'location_name': location_name,
                'latitude': coord.get('lat'),
                'longitude': coord.get('lon'),
                'temperature': main.get('temp'),
                'feels_like': main.get('feels_like'),
                'humidity': main.get('humidity'),
                'pressure': main.get('pressure'),
                'visibility': data.get('visibility', 0) / 1000 if data.get('visibility') is not None else None,  # Convert to km
                'wind_speed': wind.get('speed'),
                'wind_direction': wind.get('deg'),
                'weather_condition': weather.get('main'),
                'weather_description': weather.get('description'),
                'cloud_coverage': clouds.get('all'),
                'api_source': 'openweathermap'
            }
        except Exception as e:
            logger.error(f"Error normalizing weather data: {e}")
            raise