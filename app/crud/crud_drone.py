# backend/app/crud/crud_drone.py
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.drone import Drone
from app.schemas.drone import DroneCreate, DroneUpdate

def get_drone(db: Session, drone_id: int) -> Optional[Drone]:
    return db.query(Drone).filter(Drone.id == drone_id).first()

def get_drone_by_serial_number(db: Session, serial_number: str) -> Optional[Drone]:
    return db.query(Drone).filter(Drone.serial_number == serial_number).first()

def get_drones_by_owner(db: Session, owner_pilot_id: int, skip: int = 0, limit: int = 100) -> List[Drone]:
    return db.query(Drone).filter(Drone.owner_pilot_id == owner_pilot_id).offset(skip).limit(limit).all()

def get_all_drones(db: Session, skip: int = 0, limit: int = 100) -> List[Drone]: # For admin use
    return db.query(Drone).offset(skip).limit(limit).all()

def create_drone(db: Session, drone: DroneCreate, owner_pilot_id: int) -> Drone:
    db_drone = Drone(
        **drone.model_dump(exclude_unset=True), # Use model_dump for Pydantic v2
        owner_pilot_id=owner_pilot_id
    )
    # If drone.organization_id is not provided but pilot has an org,
    # you might want to default it to the pilot's organization.
    # For MVP, explicit assignment is fine.
    db.add(db_drone)
    db.commit()
    db.refresh(db_drone)
    return db_drone

def update_drone(db: Session, db_drone: Drone, drone_in: DroneUpdate) -> Optional[Drone]:
    update_data = drone_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_drone, field, value)
    db.add(db_drone)
    db.commit()
    db.refresh(db_drone)
    return db_drone

def delete_drone(db: Session, drone_id: int, owner_pilot_id: int) -> Optional[Drone]:
    # Ensure the drone belongs to the pilot trying to delete it (or admin)
    db_drone = db.query(Drone).filter(Drone.id == drone_id, Drone.owner_pilot_id == owner_pilot_id).first()
    if db_drone:
        db.delete(db_drone)
        db.commit()
        return db_drone
    return None

def admin_delete_drone(db: Session, drone_id: int) -> Optional[Drone]: # For admin use
    db_drone = db.query(Drone).filter(Drone.id == drone_id).first()
    if db_drone:
        db.delete(db_drone)
        db.commit()
        return db_drone
    return None