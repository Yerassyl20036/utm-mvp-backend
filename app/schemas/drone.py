# backend/app/schemas/drone.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

# Properties to receive via API on creation
class DroneCreate(BaseModel):
    model_name: str
    serial_number: str
    # hardware_id: Optional[str] = None
    organization_id: Optional[int] = None # If pilot can assign drone to their org

# Properties to return to client
class Drone(BaseModel):
    id: int
    model_name: str
    serial_number: str
    # hardware_id: Optional[str] = None
    owner_pilot_id: int
    organization_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True) # ORM mode

# Properties to receive via API on update
class DroneUpdate(BaseModel):
    model_name: Optional[str] = None
    serial_number: Optional[str] = None # Usually not updatable, but depends on rules
    # hardware_id: Optional[str] = None
    organization_id: Optional[int] = None