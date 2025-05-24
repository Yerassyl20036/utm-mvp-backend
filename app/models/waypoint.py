# backend/app/models/waypoint.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Waypoint(Base):
    flight_plan_id = Column(Integer, ForeignKey("flight_plans.id", name="fk_waypoint_flightplan_id", ondelete="CASCADE"), nullable=False) # Added ondelete
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_m = Column(Float, nullable=False) # Altitude in meters
    sequence_order = Column(Integer, nullable=False, index=True)

    # Relationship
    flight_plan = relationship("FlightPlan", back_populates="waypoints")

    def __repr__(self):
        return f"<Waypoint(id={self.id}, flight_plan_id={self.flight_plan_id}, order={self.sequence_order})>"