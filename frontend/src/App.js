import React, { useState, useEffect } from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Container, 
  Grid, 
  Card, 
  CardContent,
  Box,
  CircularProgress,
  Alert
} from '@mui/material';
import { 
  WbSunny as SunIcon,
  Cloud as CloudIcon,
  Thermostat as TempIcon,
  Air as WindIcon
} from '@mui/icons-material';
import WeatherChart from './components/WeatherChart';
import LocationsList from './components/LocationsList';
import AlertsList from './components/AlertsList';
import { weatherAPI } from './services/api';
import './App.css';

function App() {
  const [currentWeather, setCurrentWeather] = useState(null);
  const [hourlyTrends, setHourlyTrends] = useState([]);
  const [locationComparison, setLocationComparison] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchWeatherData();
    const interval = setInterval(fetchWeatherData, 15 * 60 * 1000); // 15 minutes
    return () => clearInterval(interval);
  }, []);

  const fetchWeatherData = async () => {
    try {
      setLoading(true);
      const [current, trends, comparison, alertsData] = await Promise.all([
        weatherAPI.getCurrentWeather(),
        weatherAPI.getHourlyTrends(24),
        weatherAPI.getLocationComparison(),
        weatherAPI.getAlerts()
      ]);

      setCurrentWeather(current);
      setHourlyTrends(trends);
      setLocationComparison(comparison);
      setAlerts(alertsData);
      setError(null);
    } catch (err) {
      setError('Failed to fetch weather data');
      console.error('Error fetching weather data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getWeatherIcon = (condition) => {
    const iconStyle = { fontSize: 48, color: '#FFB74D' };
    switch (condition?.toLowerCase()) {
      case 'clear':
        return <SunIcon sx={iconStyle} />;
      case 'clouds':
        return <CloudIcon sx={iconStyle} />;
      default:
        return <CloudIcon sx={iconStyle} />;
    }
  };

  return (
    <div className="App">
      <AppBar position="static" sx={{ backgroundColor: '#1976d2' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Weather Dashboard
          </Typography>
          <Typography variant="body2">
            Last updated: {new Date().toLocaleTimeString()}
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            {/* Current Weather Overview */}
            <Grid item xs={12} md={8}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h5" component="h2" gutterBottom>
                    Current Weather
                  </Typography>
                  {currentWeather ? (
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={12} sm={6}>
                        <Box display="flex" alignItems="center" gap={2}>
                          {getWeatherIcon(currentWeather.weather_condition)}
                          <Box>
                            <Typography variant="h3" component="div">
                              {currentWeather.temperature}°C
                            </Typography>
                            <Typography variant="body1" color="text.secondary">
                              Feels like {currentWeather.feels_like}°C
                            </Typography>
                            <Typography variant="h6">
                              {currentWeather.location_name}
                            </Typography>
                          </Box>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Box display="flex" flexDirection="column" gap={1}>
                          <Box display="flex" alignItems="center" gap={1}>
                            <TempIcon color="primary" />
                            <Typography>Humidity: {currentWeather.humidity}%</Typography>
                          </Box>
                          <Box display="flex" alignItems="center" gap={1}>
                            <WindIcon color="primary" />
                            <Typography>Wind: {currentWeather.wind_speed} m/s</Typography>
                          </Box>
                          <Typography variant="body2" color="text.secondary">
                            {currentWeather.weather_description}
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  ) : (
                    <Typography>No current weather data available</Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* Weather Alerts */}
            <Grid item xs={12} md={4}>
              <AlertsList alerts={alerts} />
            </Grid>

            {/* Temperature Trends Chart */}
            <Grid item xs={12} lg={8}>
              <Card>
                <CardContent>
                  <Typography variant="h5" component="h2" gutterBottom>
                    24-Hour Temperature Trend
                  </Typography>
                  <WeatherChart data={hourlyTrends} />
                </CardContent>
              </Card>
            </Grid>

            {/* Locations Comparison */}
            <Grid item xs={12} lg={4}>
              <LocationsList locations={locationComparison} />
            </Grid>
          </Grid>
        )}
      </Container>
    </div>
  );
}

export default App;