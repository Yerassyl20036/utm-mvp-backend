# backend/app/schemas/waypoint.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Annotated

class WaypointBase(BaseModel):
    latitude: Annotated[float, Field(ge=-90.0, le=90.0)]
    longitude: Annotated[float, Field(ge=-180.0, le=180.0)]
    altitude_m: float # Consider constraints, e.g., conint(ge=0, le=500)
    sequence_order: Annotated[float, Field(ge=0)]

class WaypointCreate(WaypointBase):
    pass

class Waypoint(WaypointBase):
    id: int
    flight_plan_id: int
    
    model_config = ConfigDict(from_attributes=True)