# backend/app/schemas/pilot.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Schema for creating a new pilot (registration)
class PilotCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    # organization_id: Optional[int] = None # We can add this later if registration includes org selection

# Schema for reading/returning pilot data (excluding password)
class Pilot(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
    organization_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True) # For ORM mode

# Schema for updating a pilot (if needed later)
class PilotUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    organization_id: Optional[int] = None