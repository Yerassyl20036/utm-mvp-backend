# backend/app/models/restricted_zone.py
from sqlalchemy import Column, String, Integer, Float, JSON # Or use PostGIS types if using PostGIS
from app.db.base_class import Base

class RestrictedZone(Base):
    # __tablename__ will be 'restrictedzones'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # For simple circular zones:
    center_latitude = Column(Float, nullable=True)
    center_longitude = Column(Float, nullable=True)
    radius_m = Column(Float, nullable=True)

    # For polygon zones (store as GeoJSON or list of points):
    # geometry_type = Column(String, default="POLYGON") # e.g., POINT, POLYGON, CIRCLE
    # coordinates = Column(JSON, nullable=True) # Store as GeoJSON geometry object or list of [lon, lat]
    
    min_altitude_m = Column(Float, nullable=True) # Minimum restricted altitude AGL/AMSL
    max_altitude_m = Column(Float, nullable=True) # Maximum restricted altitude AGL/AMSL

    # active_from = Column(DateTime(timezone=True), nullable=True) # For temporary zones
    # active_to = Column(DateTime(timezone=True), nullable=True)