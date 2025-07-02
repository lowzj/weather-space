"""
Locations API endpoints
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from weather_dashboard.core.database import get_db
from weather_dashboard.schemas.weather import FavoriteLocationCreate, FavoriteLocationResponse
from weather_dashboard.models.weather import FavoriteLocation

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/favorites", response_model=List[FavoriteLocationResponse])
async def get_favorite_locations(
    user_id: str = "lowzj",
    db: Session = Depends(get_db)
):
    """Get favorite locations for a user"""
    try:
        favorites = (
            db.query(FavoriteLocation)
            .filter(FavoriteLocation.user_id == user_id)
            .order_by(FavoriteLocation.is_default.desc(), FavoriteLocation.created_at)
            .all()
        )
        return favorites
    except Exception as e:
        logger.error(f"Error getting favorite locations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/favorites", response_model=FavoriteLocationResponse)
async def add_favorite_location(
    location: FavoriteLocationCreate,
    db: Session = Depends(get_db)
):
    """Add a new favorite location"""
    try:
        # Check if location already exists for this user
        existing = (
            db.query(FavoriteLocation)
            .filter(
                FavoriteLocation.user_id == location.user_id,
                FavoriteLocation.location_name == location.location_name
            )
            .first()
        )
        
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="Location already exists in favorites"
            )
        
        # If this is set as default, remove default from other locations
        if location.is_default:
            db.query(FavoriteLocation).filter(
                FavoriteLocation.user_id == location.user_id,
                FavoriteLocation.is_default == True
            ).update({FavoriteLocation.is_default: False})
        
        db_location = FavoriteLocation(**location.model_dump())
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        
        return db_location
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding favorite location: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/favorites/{location_id}")
async def remove_favorite_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    """Remove a favorite location"""
    try:
        location = db.query(FavoriteLocation).filter(
            FavoriteLocation.id == location_id
        ).first()
        
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        db.delete(location)
        db.commit()
        
        return {"message": "Location removed from favorites"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing favorite location: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/favorites/{location_id}/default")
async def set_default_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    """Set a location as default"""
    try:
        location = db.query(FavoriteLocation).filter(
            FavoriteLocation.id == location_id
        ).first()
        
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        # Remove default from other locations for this user
        db.query(FavoriteLocation).filter(
            FavoriteLocation.user_id == location.user_id,
            FavoriteLocation.is_default == True
        ).update({FavoriteLocation.is_default: False})
        
        # Set this location as default
        location.is_default = True
        db.commit()
        
        return {"message": "Location set as default"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting default location: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")