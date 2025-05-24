# backend/app/models/organization.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.base_class import Base # Make sure Base is imported

class Organization(Base):
    # __tablename__ will be 'organizations' by Base class
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    # Add other organization-specific fields here if needed

    pilots = relationship("Pilot", back_populates="organization")
    drones = relationship("Drone", back_populates="organization") # <--- COMMENT THIS OUT IF PRESENT AND DRONE NOT READY