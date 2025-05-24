# backend/app/models/drone.py
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Drone(Base):
    # __tablename__ will be 'drones' by Base class
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True, nullable=False) # e.g., "DJI Mavic 3", "Custom FPV"
    serial_number = Column(String, unique=True, index=True, nullable=False) # Or a unique registration ID
    # hardware_id = Column(String, unique=True, index=True, nullable=True) # Optional, if different from serial

    owner_pilot_id = Column(Integer, ForeignKey("pilots.id"), nullable=False)
    owner_pilot = relationship("Pilot", back_populates="drones")

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True) # If drones can belong to an org
    organization = relationship("Organization", back_populates="drones") # Add if Org model has 'drones' relationship
    flight_plans = relationship("FlightPlan", back_populates="drone")
    # flight_plans = relationship("FlightPlan", back_populates="drone") # Add when FlightPlan model is created

    # You can add other fields like:
    # weight_kg = Column(Float, nullable=True)
    # max_flight_time_min = Column(Integer, nullable=True)
    # status = Column(String, default="IDLE") # e.g., IDLE, ACTIVE, MAINTENANCE