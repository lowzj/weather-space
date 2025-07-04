"""
Weather data model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, Boolean
from sqlalchemy.sql import func
from weather_dashboard.core.database import Base


class WeatherData(Base):
    """Weather data storage table"""
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String(255), nullable=False, index=True)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    temperature = Column(Numeric(5, 2))
    feels_like = Column(Numeric(5, 2))
    humidity = Column(Integer)
    pressure = Column(Numeric(7, 2))
    visibility = Column(Numeric(5, 2))
    uv_index = Column(Numeric(3, 1))
    wind_speed = Column(Numeric(5, 2))
    wind_direction = Column(Integer)
    weather_condition = Column(String(100))
    weather_description = Column(Text)
    cloud_coverage = Column(Integer)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    api_source = Column(String(50), default="openweathermap")
    
    def __repr__(self):
        return f"<WeatherData(location='{self.location_name}', temp={self.temperature}, time='{self.recorded_at}')>"


class FavoriteLocation(Base):
    """Location favorites table"""
    __tablename__ = "favorite_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), default="lowzj", index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<FavoriteLocation(location='{self.location_name}', user='{self.user_id}')>"


class WeatherAlert(Base):
    """Weather alerts table"""
    __tablename__ = "weather_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String(255), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<WeatherAlert(location='{self.location_name}', type='{self.alert_type}', severity='{self.severity}')>"