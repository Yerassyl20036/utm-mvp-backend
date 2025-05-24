# backend/app/models/flight_plan.py
import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class FlightPlanStatus(str, enum.Enum):
    PENDING_ORG_APPROVAL = "PENDING_ORG_APPROVAL" # For Organization Pilots
    PENDING_AUTHORITY_APPROVAL = "PENDING_AUTHORITY_APPROVAL" # For Solo Pilots or after Org Admin approval
    APPROVED = "APPROVED"
    REJECTED_BY_ORG = "REJECTED_BY_ORG"
    REJECTED_BY_AUTHORITY = "REJECTED_BY_AUTHORITY"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED_BY_PILOT = "CANCELLED_BY_PILOT"
    CANCELLED_BY_ADMIN = "CANCELLED_BY_ADMIN" # Org or Authority

class FlightPlan(Base):
    user_id = Column(Integer, ForeignKey("users.id", name="fk_flightplan_user_id"), nullable=False)
    drone_id = Column(Integer, ForeignKey("drones.id", name="fk_flightplan_drone_id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", name="fk_flightplan_organization_id"), nullable=True) # If flight belongs to an org

    planned_departure_time = Column(DateTime(timezone=True), nullable=False)
    planned_arrival_time = Column(DateTime(timezone=True), nullable=False)
    
    actual_departure_time = Column(DateTime(timezone=True), nullable=True)
    actual_arrival_time = Column(DateTime(timezone=True), nullable=True)

    status = Column(SQLAlchemyEnum(FlightPlanStatus), default=None, nullable=False) # Default set by logic based on submitter
    notes = Column(String(1000), nullable=True)
    rejection_reason = Column(String(500), nullable=True)

    approved_by_organization_admin_id = Column(Integer, ForeignKey("users.id", name="fk_flightplan_org_admin_approver_id"), nullable=True)
    approved_by_authority_admin_id = Column(Integer, ForeignKey("users.id", name="fk_flightplan_auth_admin_approver_id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True) # Final approval time
    
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Relationships
    submitter_user = relationship("User", foreign_keys=[user_id], back_populates="submitted_flight_plans")
    drone = relationship("Drone", back_populates="flight_plans")
    organization = relationship("Organization") # Simple relationship to Organization table, no back_populates needed if Org doesn't list plans directly

    organization_approver = relationship("User", foreign_keys=[approved_by_organization_admin_id], back_populates="approved_org_flight_plans")
    authority_approver = relationship("User", foreign_keys=[approved_by_authority_admin_id], back_populates="approved_auth_flight_plans")

    waypoints = relationship("Waypoint", back_populates="flight_plan", cascade="all, delete-orphan", order_by="Waypoint.sequence_order", lazy="selectin")
    telemetry_logs = relationship("TelemetryLog", back_populates="flight_plan", cascade="all, delete-orphan", order_by="TelemetryLog.timestamp", lazy="dynamic")

    def __repr__(self):
        return f"<FlightPlan(id={self.id}, status='{self.status.value}')>"