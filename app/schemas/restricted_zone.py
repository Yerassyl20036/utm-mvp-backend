# backend/app/schemas/restricted_zone.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any # Any for generic JSON

class RestrictedZoneBase(BaseModel):
    name: str
    description: Optional[str] = None
    center_latitude: Optional[float] = None
    center_longitude: Optional[float] = None
    radius_m: Optional[float] = None
    # coordinates: Optional[Any] = None # For GeoJSON
    min_altitude_m: Optional[float] = None
    max_altitude_m: Optional[float] = None

class RestrictedZoneCreate(RestrictedZoneBase):
    pass

class RestrictedZone(RestrictedZoneBase):
    id: int
    model_config = ConfigDict(from_attributes=True)