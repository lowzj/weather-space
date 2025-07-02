import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Box,
  Alert
} from '@mui/material';
import {
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  ReportProblem as ReportIcon
} from '@mui/icons-material';

const AlertsList = ({ alerts }) => {
  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'extreme':
        return <ErrorIcon color="error" />;
      case 'severe':
        return <ReportIcon color="warning" />;
      case 'moderate':
        return <WarningIcon color="warning" />;
      case 'minor':
        return <InfoIcon color="info" />;
      default:
        return <InfoIcon color="info" />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'extreme':
        return 'error';
      case 'severe':
        return 'warning';
      case 'moderate':
        return 'warning';
      case 'minor':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
          Weather Alerts
        </Typography>
        {alerts && alerts.length > 0 ? (
          <List dense>
            {alerts.map((alert) => (
              <ListItem key={alert.id} alignItems="flex-start">
                <ListItemIcon>
                  {getSeverityIcon(alert.severity)}
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box display="flex" alignItems="center" gap={1} flexWrap="wrap">
                      <Typography variant="body1" fontWeight="bold">
                        {alert.title}
                      </Typography>
                      <Chip 
                        label={alert.severity} 
                        size="small" 
                        color={getSeverityColor(alert.severity)}
                      />
                    </Box>
                  }
                  secondary={
                    <Box mt={1}>
                      <Typography variant="body2" color="text.secondary">
                        {alert.location_name} - {alert.alert_type}
                      </Typography>
                      {alert.description && (
                        <Typography variant="body2" color="text.secondary" mt={0.5}>
                          {alert.description}
                        </Typography>
                      )}
                      <Typography variant="caption" color="text.secondary">
                        {alert.start_time && (
                          <>Start: {new Date(alert.start_time).toLocaleString()}</>
                        )}
                        {alert.end_time && (
                          <> | End: {new Date(alert.end_time).toLocaleString()}</>
                        )}
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            ))}
          </List>
        ) : (
          <Alert severity="success">
            No active weather alerts
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default AlertsList;