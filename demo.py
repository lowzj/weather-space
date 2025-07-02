"""
Weather Dashboard Demo Script
Demonstrates the core functionality without requiring external dependencies
"""
import sys
import json
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.insert(0, '.')

def create_sample_weather_data():
    """Create sample weather data for demonstration"""
    from weather_dashboard.schemas.weather import WeatherDataCreate
    
    sample_locations = [
        {
            "location_name": "New York,US",
            "latitude": Decimal("40.7128"),
            "longitude": Decimal("-74.0060"),
            "temperature": Decimal("22.5"),
            "feels_like": Decimal("25.1"),
            "humidity": 65,
            "pressure": Decimal("1013.25"),
            "wind_speed": Decimal("3.2"),
            "wind_direction": 180,
            "weather_condition": "Clear",
            "weather_description": "clear sky",
            "cloud_coverage": 10
        },
        {
            "location_name": "London,GB", 
            "latitude": Decimal("51.5074"),
            "longitude": Decimal("-0.1278"),
            "temperature": Decimal("18.3"),
            "feels_like": Decimal("17.8"),
            "humidity": 72,
            "pressure": Decimal("1015.40"),
            "wind_speed": Decimal("4.1"),
            "wind_direction": 225,
            "weather_condition": "Clouds",
            "weather_description": "scattered clouds",
            "cloud_coverage": 40
        },
        {
            "location_name": "Tokyo,JP",
            "latitude": Decimal("35.6762"),
            "longitude": Decimal("139.6503"),
            "temperature": Decimal("26.7"),
            "feels_like": Decimal("29.2"),
            "humidity": 78,
            "pressure": Decimal("1008.90"),
            "wind_speed": Decimal("2.1"),
            "wind_direction": 90,
            "weather_condition": "Rain",
            "weather_description": "light rain",
            "cloud_coverage": 85
        }
    ]
    
    return [WeatherDataCreate(**data) for data in sample_locations]

def create_sample_hourly_trends():
    """Create sample hourly trend data"""
    from weather_dashboard.schemas.weather import HourlyWeatherTrend
    
    trends = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(24):
        hour = base_time + timedelta(hours=i)
        # Simulate temperature variation throughout the day
        base_temp = 20 + 5 * (1 + 0.8 * ((i - 12) / 12))  # Peak around hour 12
        
        trend = HourlyWeatherTrend(
            hour=hour,
            avg_temp=Decimal(f"{base_temp:.1f}"),
            min_temp=Decimal(f"{base_temp - 2:.1f}"),
            max_temp=Decimal(f"{base_temp + 3:.1f}"),
            avg_humidity=Decimal(f"{65 + (i % 3) * 5}")
        )
        trends.append(trend)
    
    return trends

def create_sample_alerts():
    """Create sample weather alerts"""
    from weather_dashboard.schemas.weather import WeatherAlertCreate
    
    alerts = [
        WeatherAlertCreate(
            location_name="Tokyo,JP",
            alert_type="precipitation",
            severity="moderate",
            title="Heavy Rain Warning",
            description="Heavy rainfall expected in the next 6 hours. Exercise caution when traveling.",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=6)
        ),
        WeatherAlertCreate(
            location_name="New York,US",
            alert_type="temperature",
            severity="minor",
            title="High Temperature Advisory",
            description="Temperatures may exceed 30°C today. Stay hydrated.",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=12)
        )
    ]
    
    return alerts

def demo_dashboard_queries():
    """Demonstrate the dashboard SQL queries functionality"""
    print("🌤️  Weather Dashboard SQL Queries Demo")
    print("=" * 50)
    
    # Show the actual SQL queries from the requirements
    queries = {
        "Current Weather Overview": """
        SELECT 
            location_name,
            temperature,
            feels_like,
            humidity,
            weather_condition,
            weather_description,
            wind_speed,
            recorded_at
        FROM weather_data 
        WHERE recorded_at >= NOW() - INTERVAL '1 hour'
        ORDER BY recorded_at DESC
        LIMIT 1;
        """,
        
        "Hourly Temperature Trend": """
        SELECT 
            DATE_TRUNC('hour', recorded_at) as hour,
            AVG(temperature) as avg_temp,
            MIN(temperature) as min_temp,
            MAX(temperature) as max_temp,
            AVG(humidity) as avg_humidity
        FROM weather_data 
        WHERE recorded_at >= NOW() - INTERVAL '24 hours'
        GROUP BY DATE_TRUNC('hour', recorded_at)
        ORDER BY hour;
        """,
        
        "Multi-Location Comparison": """
        WITH latest_readings AS (
            SELECT DISTINCT ON (location_name) 
                location_name,
                temperature,
                humidity,
                weather_condition,
                wind_speed,
                recorded_at
            FROM weather_data 
            WHERE recorded_at >= NOW() - INTERVAL '2 hours'
            ORDER BY location_name, recorded_at DESC
        )
        SELECT * FROM latest_readings
        ORDER BY temperature DESC;
        """,
        
        "Weather Alerts Dashboard": """
        SELECT 
            alert_type,
            severity,
            title,
            description,
            location_name,
            start_time,
            end_time
        FROM weather_alerts 
        WHERE end_time > NOW() OR end_time IS NULL
        ORDER BY 
            CASE severity 
                WHEN 'extreme' THEN 1
                WHEN 'severe' THEN 2
                WHEN 'moderate' THEN 3
                WHEN 'minor' THEN 4
            END,
            start_time DESC;
        """
    }
    
    for name, query in queries.items():
        print(f"\n📊 {name}:")
        print("-" * 30)
        print(query.strip())

def demo_api_endpoints():
    """Demonstrate API endpoints"""
    print("\n\n🔌 Weather Dashboard API Endpoints")
    print("=" * 50)
    
    endpoints = {
        "Weather Data": [
            "GET /api/weather/current - Get current weather overview",
            "GET /api/weather/trends/hourly?hours=24 - Get hourly temperature trends",
            "GET /api/weather/summary/weekly?days=7 - Get weekly weather summary", 
            "GET /api/weather/comparison/locations - Get multi-location comparison",
            "GET /api/weather/history/{location} - Get weather history",
            "POST /api/weather/fetch - Manually trigger weather data fetching"
        ],
        "Locations": [
            "GET /api/locations/favorites - Get favorite locations",
            "POST /api/locations/favorites - Add favorite location",
            "DELETE /api/locations/favorites/{id} - Remove favorite location",
            "PUT /api/locations/favorites/{id}/default - Set default location"
        ],
        "Alerts": [
            "GET /api/alerts/ - Get weather alerts",
            "POST /api/alerts/ - Create weather alert",
            "GET /api/alerts/{id} - Get specific alert",
            "DELETE /api/alerts/{id} - Delete alert",
            "GET /api/alerts/location/{location} - Get alerts by location"
        ]
    }
    
    for category, endpoint_list in endpoints.items():
        print(f"\n📂 {category}:")
        for endpoint in endpoint_list:
            print(f"  • {endpoint}")

def demo_sample_data():
    """Demonstrate sample data structures"""
    print("\n\n📋 Sample Data Structures")
    print("=" * 50)
    
    # Current weather data
    current_weather = create_sample_weather_data()
    print("\n🌡️ Current Weather Data:")
    for weather in current_weather:
        data = weather.model_dump()
        print(f"  📍 {data['location_name']}: {data['temperature']}°C, {data['weather_condition']}")
    
    # Hourly trends
    trends = create_sample_hourly_trends()
    print(f"\n📈 Hourly Trends (Last 24 hours): {len(trends)} data points")
    print(f"  📊 Temperature range: {min(t.min_temp for t in trends)}°C - {max(t.max_temp for t in trends)}°C")
    
    # Alerts
    alerts = create_sample_alerts()
    print(f"\n🚨 Active Alerts: {len(alerts)} alerts")
    for alert in alerts:
        data = alert.model_dump()
        print(f"  ⚠️  {data['location_name']}: {data['title']} ({data['severity']})")

def demo_features():
    """Demonstrate key features"""
    print("\n\n✨ Key Features Implemented")
    print("=" * 50)
    
    features = [
        "✅ Real-time weather data display with 15-minute auto-refresh",
        "✅ Historical trends: temperature charts for 24h, 7d, 30d periods",
        "✅ Multi-location support with favorites management", 
        "✅ Weather alerts system with severity-based notifications",
        "✅ Mobile-responsive React frontend with Material-UI",
        "✅ FastAPI backend with comprehensive REST API",
        "✅ PostgreSQL database with optimized time-series queries",
        "✅ OpenWeatherMap API integration with error handling",
        "✅ Celery background tasks for periodic data collection",
        "✅ Docker containerization for easy deployment",
        "✅ Comprehensive API documentation with Swagger/OpenAPI",
        "✅ Production-ready configuration management"
    ]
    
    for feature in features:
        print(f"  {feature}")

def main():
    """Run the demo"""
    print("🌍 Weather Space Dashboard - Comprehensive Demo")
    print("=" * 60)
    print("This demo showcases the complete weather dashboard implementation")
    print("with all features from the original requirements.")
    
    try:
        demo_sample_data()
        demo_dashboard_queries()
        demo_api_endpoints() 
        demo_features()
        
        print("\n\n🚀 Getting Started")
        print("=" * 50)
        print("1. Copy .env.example to .env and add your OpenWeatherMap API key")
        print("2. Run: docker-compose up -d")
        print("3. Access frontend: http://localhost:3000")
        print("4. Access API docs: http://localhost:8000/docs")
        print("5. View real-time weather data and analytics!")
        
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)