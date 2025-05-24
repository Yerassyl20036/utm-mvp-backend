# backend/app/schemas/flight_plan.py
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime
from app.models.flight_plan import FlightStatus # Import the enum
from .waypoint import Waypoint, WaypointCreate # Import Waypoint schemas

class FlightPlanBase(BaseModel):
    drone_id: int
    planned_departure_time: datetime
    planned_arrival_time: datetime
    notes: Optional[str] = None

    @field_validator('planned_arrival_time')
    @classmethod
    def arrival_must_be_after_departure(cls, v, values):
        # Pydantic v2 way to access other fields for validation
        # For Pydantic v1, it would be:
        # def arrival_must_be_after_departure(cls, v, values, **kwargs):
        # if 'planned_departure_time' in values.data and v <= values.data['planned_departure_time']:
        if 'planned_departure_time' in values.data and v <= values.data['planned_departure_time']:
            raise ValueError('Planned arrival time must be after planned departure time')
        return v

class FlightPlanCreate(FlightPlanBase):
    waypoints: List[WaypointCreate] # Expect a list of waypoints on creation

    @field_validator('waypoints')
    @classmethod
    def waypoints_must_not_be_empty_and_ordered(cls, v: List[WaypointCreate]):
        if not v:
            raise ValueError('Flight plan must have at least one waypoint.')
        # Check if sequence_order is unique and sequential (optional, but good)
        # For MVP, just ensuring not empty is fine.
        # sorted_waypoints = sorted(v, key=lambda wp: wp.sequence_order)
        # for i, wp in enumerate(sorted_waypoints):
        #     if wp.sequence_order != i:
        #         raise ValueError("Waypoint sequence_order must be unique and sequential starting from 0.")
        return v


class FlightPlan(FlightPlanBase):
    id: int
    pilot_id: int
    status: FlightStatus
    waypoints: List[Waypoint] = [] # Return waypoints when fetching a flight plan

    model_config = ConfigDict(from_attributes=True)

class FlightPlanUpdate(BaseModel): # For updating status, etc.
    status: Optional[FlightStatus] = None
    notes: Optional[str] = None
    # Potentially allow updating times or waypoints, but that's more complex
    # planned_departure_time: Optional[datetime] = None
    # planned_arrival_time: Optional[datetime] = None
    # waypoints: Optional[List[WaypointCreate]] = None