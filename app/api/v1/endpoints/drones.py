# backend/app/api/v1/endpoints/drones.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.db.database import get_db
from app.deps import get_current_active_pilot, get_current_active_admin_pilot

router = APIRouter()

@router.post("/", response_model=schemas.Drone, status_code=status.HTTP_201_CREATED)
def register_new_drone(
    *,
    db: Session = Depends(get_db),
    drone_in: schemas.DroneCreate,
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Register a new drone for the current authenticated pilot.
    """
    existing_drone = crud.get_drone_by_serial_number(db, serial_number=drone_in.serial_number)
    if existing_drone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A drone with this serial number already exists."
        )
    
    # Optional: Check if organization_id (if provided) belongs to the pilot's organization
    if drone_in.organization_id and drone_in.organization_id != current_pilot.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot assign drone to an organization the pilot does not belong to."
        )
        
    drone = crud.create_drone(db=db, drone=drone_in, owner_pilot_id=current_pilot.id)
    return drone

@router.get("/", response_model=List[schemas.Drone])
def list_my_drones(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Retrieve drones registered by the current authenticated pilot.
    """
    drones = crud.get_drones_by_owner(db, owner_pilot_id=current_pilot.id, skip=skip, limit=limit)
    return drones

@router.get("/{drone_id}", response_model=schemas.Drone)
def read_drone_by_id(
    drone_id: int,
    db: Session = Depends(get_db),
    current_pilot: models.Pilot = Depends(get_current_active_pilot) # Ensures only owner or admin can see
):
    """
    Get a specific drone by ID.
    Pilot can only see their own drone. Admin can see any.
    """
    drone = crud.get_drone(db, drone_id=drone_id)
    if not drone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found")
    if drone.owner_pilot_id != current_pilot.id and not current_pilot.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this drone")
    return drone

@router.put("/{drone_id}", response_model=schemas.Drone)
def update_existing_drone(
    drone_id: int,
    *,
    db: Session = Depends(get_db),
    drone_in: schemas.DroneUpdate,
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Update a drone. Pilot can only update their own drone.
    """
    db_drone = crud.get_drone(db, drone_id=drone_id)
    if not db_drone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found")
    if db_drone.owner_pilot_id != current_pilot.id:
        # Admins could potentially update any drone, but for MVP let's restrict to owner
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this drone")
    
    # If serial number is being updated, check for uniqueness if it's allowed to change
    if drone_in.serial_number and drone_in.serial_number != db_drone.serial_number:
        existing_drone_with_new_serial = crud.get_drone_by_serial_number(db, serial_number=drone_in.serial_number)
        if existing_drone_with_new_serial and existing_drone_with_new_serial.id != drone_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A drone with this new serial number already exists."
            )
            
    # Optional: Check organization_id update logic
    if drone_in.organization_id and drone_in.organization_id != current_pilot.organization_id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot assign drone to an organization the pilot does not belong to."
        )

    updated_drone = crud.update_drone(db=db, db_drone=db_drone, drone_in=drone_in)
    return updated_drone

@router.delete("/{drone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pilot_drone(
    drone_id: int,
    db: Session = Depends(get_db),
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Delete a drone owned by the current pilot.
    """
    drone_to_delete = crud.get_drone(db, drone_id=drone_id)
    if not drone_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found")
    if drone_to_delete.owner_pilot_id != current_pilot.id:
        # For MVP, only owner can delete. Admin deletion might be a separate endpoint or logic.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this drone")
    
    deleted_drone = crud.delete_drone(db=db, drone_id=drone_id, owner_pilot_id=current_pilot.id)
    if not deleted_drone: # Should not happen if checks above pass, but good practice
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found or not owned by user")
    return None # For 204 No Content

# Example Admin endpoint (optional for MVP core)
@router.get("/admin/all", response_model=List[schemas.Drone], tags=["Admin Drones"])
def list_all_drones_admin(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin_pilot: models.Pilot = Depends(get_current_active_admin_pilot)
):
    """
    Retrieve all drones in the system (Admin only).
    """
    drones = crud.get_all_drones(db, skip=skip, limit=limit)
    return drones

@router.delete("/admin/{drone_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Admin Drones"])
def delete_any_drone_admin(
    drone_id: int,
    db: Session = Depends(get_db),
    current_admin_pilot: models.Pilot = Depends(get_current_active_admin_pilot)
):
    """
    Delete any drone in the system (Admin only).
    """
    deleted_drone = crud.admin_delete_drone(db=db, drone_id=drone_id)
    if not deleted_drone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found")
    return None