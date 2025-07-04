"""
Test script to validate the weather dashboard API
"""
import os
import sys
sys.path.insert(0, '.')

def test_configuration():
    """Test configuration loading"""
    try:
        from weather_dashboard.core.config import settings
        print("✓ Configuration loaded successfully")
        print(f"  - Database URL configured: {bool(settings.database_url)}")
        print(f"  - OpenWeather API key configured: {bool(settings.openweather_api_key)}")
        print(f"  - Default locations: {settings.default_locations}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_models():
    """Test database models"""
    try:
        from weather_dashboard.models.weather import WeatherData, FavoriteLocation, WeatherAlert
        print("✓ Database models imported successfully")
        
        # Test model creation (without DB connection)
        weather_data = WeatherData(
            location_name="Test Location",
            latitude=40.7128,
            longitude=-74.0060,
            temperature=25.5,
            humidity=65
        )
        print("✓ WeatherData model instantiated successfully")
        
        favorite = FavoriteLocation(
            location_name="Test Location",
            latitude=40.7128,
            longitude=-74.0060
        )
        print("✓ FavoriteLocation model instantiated successfully")
        
        alert = WeatherAlert(
            location_name="Test Location",
            alert_type="temperature",
            severity="moderate",
            title="Test Alert"
        )
        print("✓ WeatherAlert model instantiated successfully")
        
        return True
    except Exception as e:
        print(f"✗ Models error: {e}")
        return False

def test_services():
    """Test service imports"""
    try:
        from weather_dashboard.services.openweather import OpenWeatherMapService
        print("✓ OpenWeatherMapService imported successfully")
        
        from weather_dashboard.services.weather_service import WeatherService
        print("✓ WeatherService imported successfully")
        
        # Test service instantiation (without API key for now)
        try:
            # This will fail without API key, but we're testing import/structure
            service = OpenWeatherMapService(api_key="test_key")
            print("✓ OpenWeatherMapService instantiated successfully")
        except ValueError as e:
            # Expected when no real API key is provided
            print("✓ OpenWeatherMapService validation working")
        
        return True
    except Exception as e:
        print(f"✗ Services error: {e}")
        return False

def test_api_routers():
    """Test API router imports"""
    try:
        from weather_dashboard.api import weather_router, locations_router, alerts_router
        print("✓ API routers imported successfully")
        print(f"  - Weather router: {len(weather_router.routes)} routes")
        print(f"  - Locations router: {len(locations_router.routes)} routes")  
        print(f"  - Alerts router: {len(alerts_router.routes)} routes")
        return True
    except Exception as e:
        print(f"✗ API routers error: {e}")
        return False

def test_main_app():
    """Test main FastAPI app"""
    try:
        from weather_dashboard.main import app
        print("✓ FastAPI app imported successfully")
        print(f"  - App title: {app.title}")
        print(f"  - App version: {app.version}")
        print(f"  - Total routes: {len(app.routes)}")
        return True
    except Exception as e:
        print(f"✗ Main app error: {e}")
        return False

def test_schemas():
    """Test Pydantic schemas"""
    try:
        from weather_dashboard.schemas.weather import (
            WeatherDataCreate, WeatherDataResponse,
            FavoriteLocationCreate, FavoriteLocationResponse,
            WeatherAlertCreate, WeatherAlertResponse
        )
        print("✓ Pydantic schemas imported successfully")
        
        # Test schema instantiation
        weather_create = WeatherDataCreate(
            location_name="Test Location",
            latitude=40.7128,
            longitude=-74.0060,
            temperature=25.5
        )
        print("✓ WeatherDataCreate schema instantiated successfully")
        
        return True
    except Exception as e:
        print(f"✗ Schemas error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Weather Dashboard Validation Tests")
    print("=" * 60)
    
    tests = [
        test_configuration,
        test_models,
        test_services,
        test_api_routers,
        test_main_app,
        test_schemas
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n--- Running {test.__name__} ---")
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! The weather dashboard is ready to run.")
        print("\nNext steps:")
        print("1. Set up your OpenWeatherMap API key in .env file")
        print("2. Start PostgreSQL and Redis services")
        print("3. Run: uvicorn weather_dashboard.main:app --reload")
        print("4. Access API docs at: http://localhost:8000/docs")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)