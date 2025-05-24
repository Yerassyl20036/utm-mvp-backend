# backend/app/models/user.py
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    AUTHORITY_ADMIN = "AUTHORITY_ADMIN"
    ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN"
    ORGANIZATION_PILOT = "ORGANIZATION_PILOT"
    SOLO_PILOT = "SOLO_PILOT"

class User(Base):
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=True, index=True)
    iin = Column(String(12), unique=True, nullable=True, index=True) # Kazakhstani IIN
    hashed_password = Column(String(255), nullable=False)
    
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    
    organization_id = Column(Integer, ForeignKey("organizations.id", name="fk_user_organization_id"), nullable=True)
    is_active = Column(Boolean(), default=True, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Relationships
    organization = relationship(
        "Organization",
        back_populates="users",
        foreign_keys=[organization_id]  # Explicitly specify which foreign key to use
    )
    
    # Drones directly owned by this user (primarily for SOLO_PILOT)
    owned_drones = relationship(
        "Drone", 
        foreign_keys="[Drone.solo_owner_user_id]", # Explicit foreign keys for clarity
        back_populates="solo_owner_user", 
        cascade="all, delete-orphan"
    )
    
    # Drones assigned to this user (for ORGANIZATION_PILOT via association table)
    assigned_drones_association = relationship("UserDroneAssignment", back_populates="user", cascade="all, delete-orphan")
    
    submitted_flight_plans = relationship("FlightPlan", foreign_keys="[FlightPlan.user_id]", back_populates="submitter_user", cascade="all, delete-orphan")
    
    # Flight plans approved by this user (if they are an admin)
    approved_org_flight_plans = relationship(
        "FlightPlan", 
        foreign_keys="[FlightPlan.approved_by_organization_admin_id]",
        back_populates="organization_approver",
        lazy="dynamic" # Use dynamic if this list can be very large
    )
    approved_auth_flight_plans = relationship(
        "FlightPlan",
        foreign_keys="[FlightPlan.approved_by_authority_admin_id]",
        back_populates="authority_approver",
        lazy="dynamic"
    )
    
    created_restricted_zones = relationship(
        "RestrictedZone",
        back_populates="creator_authority",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    def __repr__(self):
        # if self.role is already an enum, use .value, otherwise assume it's a string
        role_val = self.role.value if hasattr(self.role, "value") else self.role
        return f"<User(id={self.id}, email='{self.email}', role='{role_val}')>"
    
    