# backend/app/crud/crud_pilot.py
from sqlalchemy.orm import Session
from typing import Optional

from app.models.pilot import Pilot
from app.schemas.pilot import PilotCreate
from app.core.security import get_password_hash

def get_pilot(db: Session, pilot_id: int) -> Optional[Pilot]:
    return db.query(Pilot).filter(Pilot.id == pilot_id).first()

def get_pilot_by_email(db: Session, email: str) -> Optional[Pilot]:
    return db.query(Pilot).filter(Pilot.email == email).first()

def get_pilots(db: Session, skip: int = 0, limit: int = 100) -> list[Pilot]:
    return db.query(Pilot).offset(skip).limit(limit).all()

def create_pilot(db: Session, pilot: PilotCreate) -> Pilot:
    hashed_password = get_password_hash(pilot.password)
    db_pilot = Pilot(
        email=pilot.email,
        hashed_password=hashed_password,
        name=pilot.name,
        # organization_id=pilot.organization_id # If included in PilotCreate
        is_active=True, # Default to active
        is_admin=False # Default to not admin
    )
    db.add(db_pilot)
    db.commit()
    db.refresh(db_pilot)
    return db_pilot

# Add update_pilot and delete_pilot functions later if needed