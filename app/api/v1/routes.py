# backend/app/api/v1/routes.py
from fastapi import APIRouter

from app.api.v1.endpoints import auth, pilots, drones, flights # <--- IMPORT flights

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(pilots.router, prefix="/pilots", tags=["Pilots"])
api_router.include_router(drones.router, prefix="/drones", tags=["Drones"])
api_router.include_router(flights.router, prefix="/flights", tags=["Flights"]) # <--- ADD THIS LINE