# backend/app/models/waypoint.py
from sqlalchemy import Column, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint # Import this
from app.db.base_class import Base

class Waypoint(Base):
    # __tablename__ will be 'waypoints'
    id = Column(Integer, primary_key=True, index=True) # Keep index=True for primary key
    
    # Define flight_plan_id without the ForeignKey inline
    flight_plan_id = Column(Integer, nullable=False) 
    
    flight_plan = relationship("FlightPlan", back_populates="waypoints")

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_m = Column(Float, nullable=False)
    sequence_order = Column(Integer, nullable=False)

    # Define ForeignKeyConstraint and any other table-level arguments here
    __table_args__ = (
        ForeignKeyConstraint(['flight_plan_id'], ['flight_plans.id'], name='fk_waypoint_flight_plan_id'),
        Index('ix_waypoint_flight_plan_id_sequence_order', 'flight_plan_id', 'sequence_order', unique=True) # Example composite index
    )