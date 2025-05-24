# backend/app/api/v1/endpoints/flights.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import asyncio # For background tasks

from app import crud, models, schemas
from app.db.database import get_db, SessionLocal # Import SessionLocal for the factory
from app.deps import get_current_active_pilot, get_current_active_admin_pilot
from app.utils.geospatial import check_waypoint_against_nfzs # Import our NFZ checker
from app.models.flight_plan import FlightStatus # Import FlightStatus enum
from app.services.telemetry_simulation import simulate_flight_telemetry # Import the simulation service

router = APIRouter()

@router.post("/", response_model=schemas.FlightPlan, status_code=status.HTTP_201_CREATED)
def submit_new_flight_plan(
    *,
    db: Session = Depends(get_db),
    flight_plan_in: schemas.FlightPlanCreate,
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Submit a new flight plan.
    The flight plan will be validated against No-Fly Zones.
    """
    # 1. Validate Drone Ownership (or if pilot is authorized to use the drone)
    drone = crud.get_drone(db, drone_id=flight_plan_in.drone_id)
    if not drone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drone not found.")
    if drone.owner_pilot_id != current_pilot.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Pilot not authorized to use this drone.")

    # 2. No-Fly Zone Validation for each waypoint
    for i, waypoint_data in enumerate(flight_plan_in.waypoints):
        violating_nfz = check_waypoint_against_nfzs(
            latitude=waypoint_data.latitude,
            longitude=waypoint_data.longitude,
            altitude_m=waypoint_data.altitude_m
        )
        if violating_nfz:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Waypoint {i+1} (Lat: {waypoint_data.latitude}, Lon: {waypoint_data.longitude}, Alt: {waypoint_data.altitude_m}m) "
                       f"is inside No-Fly Zone: {violating_nfz['name']}. Description: {violating_nfz.get('description', 'N/A')}"
            )

    flight_plan = crud.create_flight_plan_with_waypoints(
        db=db, flight_plan_in=flight_plan_in, pilot_id=current_pilot.id
    )
    return flight_plan


@router.get("/", response_model=List[schemas.FlightPlan])
def list_my_flight_plans(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Retrieve flight plans submitted by the current authenticated pilot.
    """
    flight_plans = crud.get_flight_plans_by_pilot(
        db, pilot_id=current_pilot.id, skip=skip, limit=limit
    )
    return flight_plans


@router.get("/{flight_plan_id}", response_model=schemas.FlightPlan)
def read_flight_plan_by_id(
    flight_plan_id: int,
    db: Session = Depends(get_db),
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Get a specific flight plan by ID.
    Pilot can only see their own flight plan. Admin can see any.
    """
    flight_plan = crud.get_flight_plan(db, flight_plan_id=flight_plan_id)
    if not flight_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight plan not found")
    
    if flight_plan.pilot_id != current_pilot.id and not current_pilot.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this flight plan"
        )
    return flight_plan


@router.put("/{flight_plan_id}/status", response_model=schemas.FlightPlan)
def update_flight_plan_status_endpoint(
    flight_plan_id: int,
    status_update: schemas.FlightPlanUpdate,
    db: Session = Depends(get_db),
    current_admin_pilot: models.Pilot = Depends(get_current_active_admin_pilot)
):
    """
    Update the status of a flight plan (e.g., approve, reject, cancel).
    (Admin Only for changing to Approved/Rejected for this example)
    """
    if status_update.status is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No status provided for update.")

    # Ensure the flight plan exists before trying to update
    existing_flight_plan = crud.get_flight_plan(db, flight_plan_id=flight_plan_id)
    if not existing_flight_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight plan not found")

    updated_flight_plan = crud.update_flight_plan_status(
        db, flight_plan_id=flight_plan_id, status=status_update.status
    )
    # crud.update_flight_plan_status should return the updated plan or None if not found.
    # The check above should prevent 'None' here unless there's a race condition or other issue.
    if not updated_flight_plan:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update flight plan status.")
    return updated_flight_plan


@router.put("/{flight_plan_id}/start", response_model=schemas.FlightPlan)
async def start_flight(
    flight_plan_id: int,
    db: Session = Depends(get_db),
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Start a flight. Changes status to ACTIVE and begins telemetry simulation.
    Only the pilot who owns the flight plan can start it if it's APPROVED.
    """
    flight_plan = crud.get_flight_plan(db, flight_plan_id=flight_plan_id)
    if not flight_plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight plan not found")
    if flight_plan.pilot_id != current_pilot.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to start this flight")
    if flight_plan.status != FlightStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Flight plan must be APPROVED to start. Current status: {flight_plan.status}"
        )

    updated_flight_plan = crud.update_flight_plan_status(db, flight_plan_id=flight_plan.id, status=FlightStatus.ACTIVE)
    if not updated_flight_plan: # Should ideally not happen if above checks pass
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update flight status to ACTIVE.")

    print(f"Scheduling telemetry simulation for flight plan ID: {updated_flight_plan.id}")
    # Pass only the ID and the SessionLocal factory itself
    asyncio.create_task(simulate_flight_telemetry(
        flight_plan_id=updated_flight_plan.id,
        db_session_factory=SessionLocal
    ))

    return updated_flight_plan


@router.delete("/{flight_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_submitted_flight_plan(
    flight_plan_id: int,
    db: Session = Depends(get_db),
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
):
    """
    Delete a flight plan. Pilot can only delete their own (if PENDING/REJECTED/CANCELLED).
    Admin might have broader delete capabilities.
    """
    flight_plan_to_delete = crud.get_flight_plan(db, flight_plan_id=flight_plan_id)
    if not flight_plan_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight plan not found")

    can_delete = False
    if flight_plan_to_delete.pilot_id == current_pilot.id:
        if flight_plan_to_delete.status in [FlightStatus.PENDING, FlightStatus.REJECTED, FlightStatus.CANCELLED]:
            can_delete = True
    
    if current_pilot.is_admin:
        can_delete = True

    if not can_delete:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this flight plan or it's in a non-deletable state.")

    if current_pilot.is_admin and flight_plan_to_delete.pilot_id != current_pilot.id:
        deleted_fp = crud.admin_delete_flight_plan(db=db, flight_plan_id=flight_plan_id)
    else:
        deleted_fp = crud.delete_flight_plan(db=db, flight_plan_id=flight_plan_id, pilot_id=current_pilot.id)

    if not deleted_fp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delete operation failed or flight plan not found for user.")
    
    return None


@router.get("/admin/all", response_model=List[schemas.FlightPlan], tags=["Admin Flights"])
def list_all_flight_plans_admin(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin_pilot: models.Pilot = Depends(get_current_active_admin_pilot)
):
    """
    Retrieve all flight plans in the system (Admin only).
    """
    flight_plans = crud.get_all_flight_plans(db, skip=skip, limit=limit)
    return flight_plans