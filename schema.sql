-- Weather Dashboard Database Schema
-- This script creates the database schema as specified in the requirements

-- Weather data storage table
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    temperature DECIMAL(5, 2),
    feels_like DECIMAL(5, 2),
    humidity INTEGER,
    pressure DECIMAL(7, 2),
    visibility DECIMAL(5, 2),
    uv_index DECIMAL(3, 1),
    wind_speed DECIMAL(5, 2),
    wind_direction INTEGER,
    weather_condition VARCHAR(100),
    weather_description TEXT,
    cloud_coverage INTEGER,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    api_source VARCHAR(50) DEFAULT 'openweathermap'
);

-- Location favorites table
CREATE TABLE IF NOT EXISTS favorite_locations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) DEFAULT 'lowzj',
    location_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather alerts table
CREATE TABLE IF NOT EXISTS weather_alerts (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_weather_data_location ON weather_data(location_name);
CREATE INDEX IF NOT EXISTS idx_weather_data_recorded_at ON weather_data(recorded_at);
CREATE INDEX IF NOT EXISTS idx_favorite_locations_user_id ON favorite_locations(user_id);
CREATE INDEX IF NOT EXISTS idx_weather_alerts_location ON weather_alerts(location_name);
CREATE INDEX IF NOT EXISTS idx_weather_alerts_severity ON weather_alerts(severity);

-- Insert some default favorite locations
INSERT INTO favorite_locations (location_name, latitude, longitude, is_default) 
VALUES 
    ('New York,US', 40.7128, -74.0060, TRUE),
    ('London,GB', 51.5074, -0.1278, FALSE),
    ('Tokyo,JP', 35.6762, 139.6503, FALSE),
    ('Sydney,AU', -33.8688, 151.2093, FALSE)
ON CONFLICT DO NOTHING;