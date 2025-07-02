weather_dashboard/
├── __init__.py
├── main.py
├── api/
│   ├── __init__.py
│   ├── weather.py
│   ├── locations.py
│   └── alerts.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── security.py
├── models/
│   ├── __init__.py
│   ├── weather.py
│   ├── location.py
│   └── alert.py
├── services/
│   ├── __init__.py
│   ├── weather_service.py
│   ├── openweather.py
│   └── alert_service.py
├── schemas/
│   ├── __init__.py
│   ├── weather.py
│   ├── location.py
│   └── alert.py
└── tasks/
    ├── __init__.py
    ├── celery_app.py
    └── weather_tasks.py