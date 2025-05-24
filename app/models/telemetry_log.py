# backend/app/models/telemetry_log.py
from sqlalchemy import (BigInteger, Column, DateTime, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class TelemetryLog(Base):
    # Override id for BigInteger if high frequency telemetry is expected
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    flight_plan_id = Column(
        Integer,
        ForeignKey(
            "flight_plans.id", name="fk_telemetry_flightplan_id", ondelete="SET NULL"
        ),
        nullable=True,
        index=True,
    )
    drone_id = Column(
        Integer,
        ForeignKey("drones.id", name="fk_telemetry_drone_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_m = Column(Float, nullable=False)  # Altitude in meters
    speed_mps = Column(Float, nullable=True)  # Speed in meters per second
    heading_degrees = Column(Float, nullable=True)  # 0-359.9, North is 0
    status_message = Column(
        String(255), nullable=True
    )  # e.g., "ON_SCHEDULE", "NFZ_ALERT: Parliament", "SIGNAL_LOST_SIMULATED"

    # Relationships
    flight_plan = relationship("FlightPlan", back_populates="telemetry_logs")
    drone = relationship(
        "Drone",
        foreign_keys=[drone_id],
        back_populates="telemetry_logs",
        primaryjoin="TelemetryLog.drone_id == Drone.id",
    )

    def __repr__(self):
        return f"<TelemetryLog(id={self.id}, flight_plan_id={self.flight_plan_id}, ts='{self.timestamp}')>"
