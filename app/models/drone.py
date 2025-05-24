# backend/app/models/drone.py
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class DroneOwnerType(str, enum.Enum):
    ORGANIZATION = "ORGANIZATION"
    SOLO_PILOT = "SOLO_PILOT"

class DroneStatus(str, enum.Enum):
    IDLE = "IDLE"           # Available, not flying
    ACTIVE = "ACTIVE"         # Currently on an active flight
    MAINTENANCE = "MAINTENANCE" # Undergoing maintenance
    UNKNOWN = "UNKNOWN"       # Status cannot be determined (e.g., signal loss prolonged)
    # Consider adding more specific error/alert statuses if needed at drone level

class Drone(Base):
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True, index=True, nullable=False)
    
    owner_type = Column(SQLAlchemyEnum(DroneOwnerType), nullable=False)
    
    # If owned by an organization
    organization_id = Column(Integer, ForeignKey("organizations.id", name="fk_drone_organization_id"), nullable=True)
    organization_owner = relationship("Organization", foreign_keys=[organization_id], back_populates="drones")

    # If owned by a solo pilot
    solo_owner_user_id = Column(Integer, ForeignKey("users.id", name="fk_drone_solo_owner_user_id"), nullable=True)
    solo_owner_user = relationship("User", foreign_keys=[solo_owner_user_id], back_populates="owned_drones")
    
    current_status = Column(SQLAlchemyEnum(DroneStatus), default=DroneStatus.IDLE, nullable=False)
    last_telemetry_id = Column(Integer, ForeignKey("telemetry_logs.id", name="fk_drone_last_telemetry_id", use_alter=True), nullable=True) # use_alter for potential circular dep
    last_seen_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Relationships
    assigned_users_association = relationship("UserDroneAssignment", back_populates="drone", cascade="all, delete-orphan")
    flight_plans = relationship("FlightPlan", back_populates="drone", cascade="all, delete-orphan")
    telemetry_logs = relationship("TelemetryLog", back_populates="drone", cascade="all, delete-orphan", lazy="dynamic") # Can be many

    # last_telemetry_point = relationship("TelemetryLog", foreign_keys=[last_telemetry_id], post_update=True) # post_update for circular dep if needed

    def __repr__(self):
        return f"<Drone(id={self.id}, serial_number='{self.serial_number}')>"