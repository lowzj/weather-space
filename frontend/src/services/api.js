import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const weatherAPI = {
  getCurrentWeather: async () => {
    try {
      const response = await api.get('/weather/current');
      return response.data;
    } catch (error) {
      console.error('Error fetching current weather:', error);
      throw error;
    }
  },

  getHourlyTrends: async (hours = 24) => {
    try {
      const response = await api.get(`/weather/trends/hourly?hours=${hours}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching hourly trends:', error);
      throw error;
    }
  },

  getWeeklySummary: async (days = 7) => {
    try {
      const response = await api.get(`/weather/summary/weekly?days=${days}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching weekly summary:', error);
      throw error;
    }
  },

  getLocationComparison: async (hours = 2) => {
    try {
      const response = await api.get(`/weather/comparison/locations?hours=${hours}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching location comparison:', error);
      throw error;
    }
  },

  getWeatherHistory: async (location, days = 30) => {
    try {
      const response = await api.get(`/weather/history/${encodeURIComponent(location)}?days=${days}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching weather history:', error);
      throw error;
    }
  },

  fetchWeatherData: async (locations) => {
    try {
      const response = await api.post('/weather/fetch', null, {
        params: { locations }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching weather data:', error);
      throw error;
    }
  },

  getAlerts: async (activeOnly = true) => {
    try {
      const response = await api.get(`/alerts/?active_only=${activeOnly}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching alerts:', error);
      throw error;
    }
  },

  getFavoriteLocations: async (userId = 'lowzj') => {
    try {
      const response = await api.get(`/locations/favorites?user_id=${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching favorite locations:', error);
      throw error;
    }
  },

  addFavoriteLocation: async (location) => {
    try {
      const response = await api.post('/locations/favorites', location);
      return response.data;
    } catch (error) {
      console.error('Error adding favorite location:', error);
      throw error;
    }
  },

  removeFavoriteLocation: async (locationId) => {
    try {
      const response = await api.delete(`/locations/favorites/${locationId}`);
      return response.data;
    } catch (error) {
      console.error('Error removing favorite location:', error);
      throw error;
    }
  }
};

export default api;