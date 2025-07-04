"""
API endpoints initialization
"""
from .weather import router as weather_router
from .locations import router as locations_router
from .alerts import router as alerts_router

__all__ = ["weather_router", "locations_router", "alerts_router"]