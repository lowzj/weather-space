"""
Core configuration settings for the weather dashboard
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Database settings
    database_url: str = "postgresql://weather_user:weather_password@localhost:5432/weather_db"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "weather_db"
    db_user: str = "weather_user"
    db_password: str = "weather_password"
    
    # API settings
    openweather_api_key: str = ""
    openweather_base_url: str = "http://api.openweathermap.org/data/2.5"
    
    # Redis settings
    redis_url: str = "redis://localhost:6379/0"
    
    # Application settings
    secret_key: str = "your-secret-key-here"
    debug: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Weather collection settings
    fetch_interval_minutes: int = 15
    default_locations: List[str] = ["New York,US", "London,GB", "Tokyo,JP", "Sydney,AU"]
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "weather_dashboard.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()