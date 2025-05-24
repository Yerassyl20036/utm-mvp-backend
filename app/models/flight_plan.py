# backend/app/models/flight_plan.py
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Enum as SQLAlchemyEnum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint # Import this
import enum

from app.db.base_class import Base

class FlightStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class FlightPlan(Base):
    id = Column(Integer, primary_key=True, index=True)
    
    pilot_id = Column(Integer, nullable=False)
    pilot = relationship("Pilot", back_populates="flight_plans")

    drone_id = Column(Integer, nullable=False)
    drone = relationship("Drone", back_populates="flight_plans")

    planned_departure_time = Column(DateTime(timezone=True), nullable=False)
    planned_arrival_time = Column(DateTime(timezone=True), nullable=False)

    status = Column(SQLAlchemyEnum(FlightStatus), default=FlightStatus.PENDING, nullable=False)
    notes = Column(String, nullable=True)

    waypoints = relationship("Waypoint", back_populates="flight_plan", cascade="all, delete-orphan", order_by="Waypoint.sequence_order")

    __table_args__ = (
        ForeignKeyConstraint(['pilot_id'], ['pilots.id'], name='fk_flightplan_pilot_id'),
        ForeignKeyConstraint(['drone_id'], ['drones.id'], name='fk_flightplan_drone_id'),
        Index('ix_flightplan_pilot_id', 'pilot_id'),
        Index('ix_flightplan_drone_id', 'drone_id'),
        Index('ix_flightplan_status', 'status'),
    )