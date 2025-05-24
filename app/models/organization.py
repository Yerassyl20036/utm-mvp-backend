# backend/app/models/organization.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Organization(Base):
    name = Column(String(255), unique=True, index=True, nullable=False)
    bin = Column(String(12), unique=True, index=True, nullable=False) # Business Identification Number
    company_address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    
    # The primary admin user for this organization
    admin_id = Column(Integer, ForeignKey("users.id", name="fk_organization_admin_id"), nullable=True, unique=True)
    
    is_active = Column(Boolean(), default=True, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Relationships
    # admin_user = relationship("User", foreign_keys=[admin_id]) # If needed, define carefully to avoid cycles
    
    users = relationship("User", back_populates="organization", foreign_keys="[User.organization_id]")
    
    # Drones directly owned by this organization
    drones = relationship("Drone", foreign_keys="[Drone.organization_id]", back_populates="organization_owner", cascade="all, delete-orphan")
    
    # Flight plans associated with this organization (via its pilots/drones)
    # This is an indirect relationship, usually queried through User or Drone.
    # If a direct link is needed on FlightPlan, add organization_id FK there.

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"