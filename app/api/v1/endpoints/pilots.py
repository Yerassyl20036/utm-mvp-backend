# backend/app/api/v1/endpoints/pilots.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.database import get_db
from app.deps import get_current_active_pilot, get_current_active_admin_pilot

router = APIRouter()

@router.get("/me", response_model=schemas.Pilot)
def read_pilot_me(
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Get current pilot.
    """
    return current_pilot

# Example of an admin-only route (we'll need to set is_admin manually in DB for testing)
@router.get("/", response_model=List[schemas.Pilot])
def read_pilots(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin_pilot: models.Pilot = Depends(get_current_active_admin_pilot) # Ensures only admin can access
):
    """
    Retrieve all pilots. (Admin only)
    """
    pilots = crud.get_pilots(db, skip=skip, limit=limit)
    return pilots

# You might add endpoints to update pilot info here later
# e.g., PUT /me