"""
Alerts API endpoints
"""
import logging
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from weather_dashboard.core.database import get_db
from weather_dashboard.schemas.weather import WeatherAlertCreate, WeatherAlertResponse
from weather_dashboard.models.weather import WeatherAlert

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=List[WeatherAlertResponse])
async def get_weather_alerts(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get weather alerts"""
    try:
        query = db.query(WeatherAlert)
        
        if active_only:
            query = query.filter(
                or_(
                    WeatherAlert.end_time > datetime.utcnow(),
                    WeatherAlert.end_time.is_(None)
                )
            )
        
        alerts = query.order_by(
            WeatherAlert.severity.desc(),
            WeatherAlert.start_time.desc()
        ).all()
        
        return alerts
    except Exception as e:
        logger.error(f"Error getting weather alerts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=WeatherAlertResponse)
async def create_weather_alert(
    alert: WeatherAlertCreate,
    db: Session = Depends(get_db)
):
    """Create a new weather alert"""
    try:
        db_alert = WeatherAlert(**alert.model_dump())
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        
        return db_alert
    except Exception as e:
        logger.error(f"Error creating weather alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{alert_id}", response_model=WeatherAlertResponse)
async def get_weather_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific weather alert"""
    try:
        alert = db.query(WeatherAlert).filter(
            WeatherAlert.id == alert_id
        ).first()
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return alert
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting weather alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{alert_id}")
async def delete_weather_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Delete a weather alert"""
    try:
        alert = db.query(WeatherAlert).filter(
            WeatherAlert.id == alert_id
        ).first()
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        db.delete(alert)
        db.commit()
        
        return {"message": "Alert deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting weather alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/location/{location_name}", response_model=List[WeatherAlertResponse])
async def get_alerts_by_location(
    location_name: str,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get weather alerts for a specific location"""
    try:
        query = db.query(WeatherAlert).filter(
            WeatherAlert.location_name == location_name
        )
        
        if active_only:
            query = query.filter(
                or_(
                    WeatherAlert.end_time > datetime.utcnow(),
                    WeatherAlert.end_time.is_(None)
                )
            )
        
        alerts = query.order_by(
            WeatherAlert.severity.desc(),
            WeatherAlert.start_time.desc()
        ).all()
        
        return alerts
    except Exception as e:
        logger.error(f"Error getting alerts for location {location_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")