# backend/app/schemas/organization.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
# from .pilot import Pilot # To avoid circular import if Organization returns Pilots, handle carefully

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    # pilots: List[Pilot] = [] # Example if you want to nest pilot info

    model_config = ConfigDict(from_attributes=True)

class OrganizationUpdate(OrganizationBase):
    name: Optional[str] = None