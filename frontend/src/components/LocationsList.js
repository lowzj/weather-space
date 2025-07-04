import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  Box,
  Chip,
  Divider
} from '@mui/material';
import {
  LocationOn as LocationIcon,
  Thermostat as TempIcon
} from '@mui/icons-material';

const LocationsList = ({ locations }) => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
          Location Comparison
        </Typography>
        {locations && locations.length > 0 ? (
          <List dense>
            {locations.map((location, index) => (
              <React.Fragment key={index}>
                <ListItem>
                  <ListItemText
                    primary={
                      <Box display="flex" alignItems="center" gap={1}>
                        <LocationIcon color="primary" fontSize="small" />
                        <Typography variant="body1" fontWeight="bold">
                          {location.location_name}
                        </Typography>
                      </Box>
                    }
                    secondary={
                      <Box mt={1}>
                        <Box display="flex" alignItems="center" gap={1} mb={0.5}>
                          <TempIcon fontSize="small" />
                          <Typography variant="body2">
                            {location.temperature}°C
                          </Typography>
                          <Chip 
                            label={location.weather_condition || 'N/A'} 
                            size="small" 
                            variant="outlined"
                          />
                        </Box>
                        <Typography variant="caption" color="text.secondary">
                          Humidity: {location.humidity}% | Wind: {location.wind_speed} m/s
                        </Typography>
                        <br />
                        <Typography variant="caption" color="text.secondary">
                          Updated: {new Date(location.recorded_at).toLocaleString()}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
                {index < locations.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        ) : (
          <Typography variant="body2" color="text.secondary">
            No location data available
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default LocationsList;