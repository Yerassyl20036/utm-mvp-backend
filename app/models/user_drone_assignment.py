# backend/app/models/user_drone_assignment.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base # Base already has created_at, updated_at. Not strictly needed here unless desired.

class UserDroneAssignment(Base): # Inheriting from Base gives id, created_at, updated_at
    # If you don't want a surrogate PK 'id' from Base for an association table:
    # __tablename__ = "user_drone_assignments"
    # user_id = Column(Integer, ForeignKey("users.id", name="fk_userdrone_user_id"), primary_key=True)
    # drone_id = Column(Integer, ForeignKey("drones.id", name="fk_userdrone_drone_id"), primary_key=True)
    # assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # 
    # user = relationship("User", back_populates="assigned_drones_association")
    # drone = relationship("Drone", back_populates="assigned_users_association")

    # Simpler if Base provides `id` as PK, then these are just FKs.
    # However, standard M2M usually has composite PK on the FKs.
    # Let's redefine to be more standard M2M without inheriting `id` from Base for this table.

    __tablename__ = "user_drone_assignments" # Explicit table name
    user_id = Column(Integer, ForeignKey("users.id", name="fk_assignment_user_id"), primary_key=True)
    drone_id = Column(Integer, ForeignKey("drones.id", name="fk_assignment_drone_id"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # revoked_at = Column(DateTime(timezone=True), nullable=True) # For history of assignments

    user = relationship("User", back_populates="assigned_drones_association")
    drone = relationship("Drone", back_populates="assigned_users_association")

    # PrimaryKeyConstraint('user_id', 'drone_id', name='pk_user_drone_assignment') # Defined by primary_key=True on columns

    def __repr__(self):
        return f"<UserDroneAssignment(user_id={self.user_id}, drone_id={self.drone_id})>"