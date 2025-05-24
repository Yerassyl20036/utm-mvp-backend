# backend/app/models/restricted_zone.py
import enum

from sqlalchemy import JSON, Boolean, Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class NFZGeometryType(str, enum.Enum):
    CIRCLE = "CIRCLE"
    POLYGON = "POLYGON"
    # RECTANGLE could be a special case of POLYGON or handled separately


class RestrictedZone(Base):
    name = Column(String(255), index=True, nullable=False)
    description = Column(String(1000), nullable=True)

    geometry_type = Column(SQLAlchemyEnum(NFZGeometryType), nullable=False)
    # Store geometry definition as JSON. Structure depends on geometry_type.
    # For CIRCLE: {"center_lat": float, "center_lon": float, "radius_m": float}
    # For POLYGON: {"coordinates": [[[lon, lat], [lon, lat], ...]]} (GeoJSON Polygon format)
    definition_json = Column(JSON, nullable=False)

    min_altitude_m = Column(Float, nullable=True)  # AGL or AMSL - must be consistent
    max_altitude_m = Column(Float, nullable=True)

    is_active = Column(Boolean(), default=True, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

    created_by_authority_id = Column(
        Integer, ForeignKey("users.id", name="fk_nfz_creator_id"), nullable=False
    )
    creator_authority = relationship("User", back_populates="created_restricted_zones")

    def __repr__(self):
        return f"<RestrictedZone(id={self.id}, name='{self.name}')>"
