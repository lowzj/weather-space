# Weather Dashboard

A comprehensive weather dashboard with public API integration that fetches real-time weather data from OpenWeatherMap API and stores it in a PostgreSQL database for analytics and visualization.

## Features

- **Real-time Weather Display**: Current temperature, conditions, and key metrics with auto-refresh every 15 minutes
- **Historical Trends**: Temperature charts for last 24 hours, 7 days, 30 days with humidity and pressure trends
- **Multi-Location Support**: Favorite locations management and side-by-side comparison view
- **Weather Alerts**: Severe weather notifications and custom alert thresholds
- **Analytics Dashboard**: Weather pattern analysis and monthly/seasonal summaries
- **Mobile-Responsive Design**: Optimized for all device sizes

## Tech Stack

- **Backend**: Python with FastAPI
- **Database**: PostgreSQL with time-series optimization
- **API**: OpenWeatherMap API integration
- **Frontend**: React with Material-UI and Chart.js
- **Task Queue**: Celery with Redis
- **Deployment**: Docker and Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenWeatherMap API key (get one at https://openweathermap.org/api)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lowzj/weather-space.git
   cd weather-space
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenWeatherMap API key
   ```

3. **Start the application**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - API Alternative Docs: http://localhost:8000/redoc

### Manual Setup (without Docker)

1. **Database Setup**:
   ```bash
   # Install PostgreSQL and create database
   createdb weather_db
   psql weather_db < schema.sql
   ```

2. **Backend Setup**:
   ```bash
   pip install -e .
   cd weather_dashboard
   uvicorn main:app --reload
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Celery Workers** (optional):
   ```bash
   # Terminal 1: Worker
   celery -A weather_dashboard.tasks.celery_app worker --loglevel=info
   
   # Terminal 2: Beat scheduler
   celery -A weather_dashboard.tasks.celery_app beat --loglevel=info
   ```

## API Endpoints

### Weather Data
- `GET /api/weather/current` - Get current weather overview
- `GET /api/weather/trends/hourly` - Get hourly temperature trends
- `GET /api/weather/summary/weekly` - Get weekly weather summary
- `GET /api/weather/comparison/locations` - Get multi-location comparison
- `GET /api/weather/history/{location}` - Get weather history for a location
- `POST /api/weather/fetch` - Manually trigger weather data fetching

### Locations
- `GET /api/locations/favorites` - Get favorite locations
- `POST /api/locations/favorites` - Add favorite location
- `DELETE /api/locations/favorites/{id}` - Remove favorite location
- `PUT /api/locations/favorites/{id}/default` - Set default location

### Alerts
- `GET /api/alerts/` - Get weather alerts
- `POST /api/alerts/` - Create weather alert
- `GET /api/alerts/{id}` - Get specific alert
- `DELETE /api/alerts/{id}` - Delete alert
- `GET /api/alerts/location/{location}` - Get alerts by location

## Database Schema

The application uses three main tables:

### weather_data
Stores real-time weather data from the API:
- Location information (name, coordinates)
- Temperature metrics (current, feels-like)
- Weather conditions and descriptions
- Wind and atmospheric data
- Timestamps and API source

### favorite_locations
Manages user's favorite locations:
- User ID and location details
- Coordinates for API calls
- Default location settings

### weather_alerts
Stores weather alerts and notifications:
- Alert types and severity levels
- Location-specific alerts
- Time ranges and descriptions

## Dashboard Queries

The application includes optimized SQL queries for:

1. **Current Weather Overview**: Latest readings within 1 hour
2. **Hourly Temperature Trend**: Aggregated data for 24-hour periods
3. **Weekly Weather Summary**: Daily averages and extremes
4. **Multi-Location Comparison**: Latest readings across locations
5. **Weather Alerts Dashboard**: Active alerts ordered by severity

## Configuration

Key configuration options in `.env`:

- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection for Celery
- `FETCH_INTERVAL_MINUTES`: How often to fetch weather data (default: 15)
- `DEFAULT_LOCATIONS`: Comma-separated list of default locations

## Development

### Running Tests

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
black weather_dashboard/
isort weather_dashboard/
flake8 weather_dashboard/

# Frontend linting
cd frontend
npm run lint
```

### Database Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Deployment

### Production Setup

1. Update environment variables for production
2. Set `DEBUG=False` in configuration
3. Use a production WSGI server like Gunicorn
4. Set up proper database credentials and connection pooling
5. Configure Redis for Celery in production mode
6. Set up monitoring and logging

### Docker Production

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the application logs for debugging