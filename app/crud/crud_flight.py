# backend/app/crud/crud_flight.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.flight_plan import FlightPlan, FlightStatus
from app.models.waypoint import Waypoint
from app.schemas.flight_plan import FlightPlanCreate, FlightPlanUpdate
from app.schemas.waypoint import WaypointCreate

def get_flight_plan(db: Session, flight_plan_id: int) -> Optional[FlightPlan]:
    return db.query(FlightPlan).filter(FlightPlan.id == flight_plan_id).first()

def get_flight_plans_by_pilot(db: Session, pilot_id: int, skip: int = 0, limit: int = 100) -> List[FlightPlan]:
    return db.query(FlightPlan).filter(FlightPlan.pilot_id == pilot_id).order_by(FlightPlan.planned_departure_time.desc()).offset(skip).limit(limit).all()

def get_all_flight_plans(db: Session, skip: int = 0, limit: int = 100) -> List[FlightPlan]: # For admin
    return db.query(FlightPlan).order_by(FlightPlan.planned_departure_time.desc()).offset(skip).limit(limit).all()

def create_flight_plan_with_waypoints(db: Session, flight_plan_in: FlightPlanCreate, pilot_id: int) -> FlightPlan:
    # Create FlightPlan object without waypoints first
    db_flight_plan = FlightPlan(
        pilot_id=pilot_id,
        drone_id=flight_plan_in.drone_id,
        planned_departure_time=flight_plan_in.planned_departure_time,
        planned_arrival_time=flight_plan_in.planned_arrival_time,
        notes=flight_plan_in.notes,
        status=FlightStatus.PENDING # Initial status
    )
    db.add(db_flight_plan)
    # It's often better to flush here to get db_flight_plan.id if not using autoincrement properly or for immediate use
    # db.flush() # If you need the ID before commit for some reason

    # Create Waypoint objects and associate them
    db_waypoints = []
    for waypoint_in in flight_plan_in.waypoints:
        db_waypoint = Waypoint(
            **waypoint_in.model_dump(),
            flight_plan_id=db_flight_plan.id # Associate with the flight plan
        )
        db_waypoints.append(db_waypoint)
    
    db_flight_plan.waypoints = db_waypoints # Assign the list of waypoints to the relationship
                                            # SQLAlchemy will handle associating them once db_flight_plan has an ID.

    # Commit everything together (FlightPlan and its Waypoints)
    try:
        db.commit()
        db.refresh(db_flight_plan) # Refresh to get all populated fields, including waypoints
        # db.refresh() can be tricky with relationships if not configured perfectly
        # explicit query after commit can be more reliable for nested data if refresh fails
        # refreshed_plan = db.query(FlightPlan).options(joinedload(FlightPlan.waypoints)).filter(FlightPlan.id == db_flight_plan.id).first()

    except Exception as e:
        db.rollback()
        raise e
    
    return db_flight_plan


def update_flight_plan_status(db: Session, flight_plan_id: int, status: FlightStatus) -> Optional[FlightPlan]:
    db_flight_plan = get_flight_plan(db, flight_plan_id=flight_plan_id)
    if db_flight_plan:
        db_flight_plan.status = status
        db.commit()
        db.refresh(db_flight_plan)
    return db_flight_plan

def update_flight_plan(db: Session, db_flight_plan: FlightPlan, flight_plan_in: FlightPlanUpdate) -> Optional[FlightPlan]:
    update_data = flight_plan_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_flight_plan, field, value)
    db.add(db_flight_plan)
    db.commit()
    db.refresh(db_flight_plan)
    return db_flight_plan


def delete_flight_plan(db: Session, flight_plan_id: int, pilot_id: int) -> Optional[FlightPlan]:
    # Ensure pilot owns the flight plan or is admin
    db_flight_plan = db.query(FlightPlan).filter(FlightPlan.id == flight_plan_id, FlightPlan.pilot_id == pilot_id).first()
    if db_flight_plan:
        # Waypoints should be deleted automatically due to cascade="all, delete-orphan"
        db.delete(db_flight_plan)
        db.commit()
        return db_flight_plan
    return None

def admin_delete_flight_plan(db: Session, flight_plan_id: int) -> Optional[FlightPlan]:
    db_flight_plan = get_flight_plan(db, flight_plan_id=flight_plan_id)
    if db_flight_plan:
        db.delete(db_flight_plan)
        db.commit()
        return db_flight_plan
    return None

# CRUD for Waypoints individually (less common, usually managed via FlightPlan)
def create_waypoint(db: Session, waypoint: WaypointCreate, flight_plan_id: int) -> Waypoint:
    db_waypoint = Waypoint(**waypoint.model_dump(), flight_plan_id=flight_plan_id)
    db.add(db_waypoint)
    db.commit()
    db.refresh(db_waypoint)
    return db_waypoint