# backend/app/models/pilot.py
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base # Make sure Base is imported

class Pilot(Base):
    # __tablename__ will be 'pilots' by Base class
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False) # Simple role for now

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True) # Nullable if pilots can exist without org
    organization = relationship("Organization", back_populates="pilots")

    # Comment out relationships to models not yet fully defined or imported
    drones = relationship("Drone", back_populates="owner_pilot") 
    flight_plans = relationship("FlightPlan", back_populates="pilot") # Also comment if FlightPlan not done