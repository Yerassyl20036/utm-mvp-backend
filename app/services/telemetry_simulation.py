# backend/app/services/telemetry_simulation.py
import asyncio
import time
import math
from typing import List, Type, Optional # Added Optional
from sqlalchemy.orm import Session, joinedload # Import joinedload

from app.models.flight_plan import FlightPlan, FlightStatus
from app.models.waypoint import Waypoint # Ensure Waypoint is imported
from app.websockets.connection_manager import manager as ws_manager
from app.db.database import SessionLocal # For type hinting the factory
from app import crud

# Simulation parameters
SIMULATION_SPEED_MPS = 20  # meters per second
TELEMETRY_INTERVAL_S = 1   # seconds between telemetry updates

def calculate_intermediate_point(
    lat1: float, lon1: float, lat2: float, lon2: float, fraction: float, alt1: float, alt2: float
) -> tuple[float, float, float]:
    """Linearly interpolate between two geo-coordinates and altitudes."""
    lat = lat1 + (lat2 - lat1) * fraction
    lon = lon1 + (lon2 - lon1) * fraction
    alt = alt1 + (alt2 - alt1) * fraction
    return lat, lon, alt

def haversine_distance_simple(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

async def simulate_flight_telemetry(flight_plan_id: int, db_session_factory: Type[SessionLocal]):
    """
    Simulates a flight along its waypoints and broadcasts telemetry.
    Accepts a flight_plan_id and a factory to create new DB sessions.
    """
    print(f"Telemetry simulation task started for Flight ID: {flight_plan_id}")

    db: Session = db_session_factory()
    try:
        # Fetch the flight plan with its waypoints eagerly using the new session
        flight_plan_with_waypoints: Optional[FlightPlan] = (
            db.query(FlightPlan)
            .options(joinedload(FlightPlan.waypoints)) # Eagerly load waypoints
            .filter(FlightPlan.id == flight_plan_id)
            .first()
        )

        if not flight_plan_with_waypoints:
            print(f"Error: Flight plan {flight_plan_id} not found in simulation task.")
            return
        
        # Ensure waypoints are sorted by sequence_order
        # The relationship's order_by should handle this, but being explicit is safer.
        waypoints: List[Waypoint] = sorted(flight_plan_with_waypoints.waypoints, key=lambda wp: wp.sequence_order)

        if not waypoints:
            print(f"Flight ID {flight_plan_with_waypoints.id} has no waypoints. Simulation ending.")
            # Use the local db session for CRUD operations
            fp_to_complete = crud.get_flight_plan(db, flight_plan_with_waypoints.id)
            if fp_to_complete:
                 crud.update_flight_plan_status(db, flight_plan_id=fp_to_complete.id, status=FlightStatus.COMPLETED)
            # crud.update_flight_plan_status already commits if successful
            return

        current_lat = waypoints[0].latitude
        current_lon = waypoints[0].longitude
        current_alt = waypoints[0].altitude_m
        
        await ws_manager.broadcast_json({
            "flightId": flight_plan_with_waypoints.id,
            "droneId": flight_plan_with_waypoints.drone_id,
            "lat": current_lat, "lon": current_lon, "alt": current_alt,
            "timestamp": time.time(), "status": "ON_SCHEDULE", "waypoint_idx": 0
        })

        for i in range(len(waypoints) - 1):
            start_wp = waypoints[i]
            end_wp = waypoints[i+1]

            distance_m = haversine_distance_simple(
                start_wp.latitude, start_wp.longitude,
                end_wp.latitude, end_wp.longitude
            )
            
            time_to_travel_s = distance_m / SIMULATION_SPEED_MPS if SIMULATION_SPEED_MPS > 0 else float('inf')
            num_steps = max(1, int(time_to_travel_s / TELEMETRY_INTERVAL_S)) if TELEMETRY_INTERVAL_S > 0 else 1

            for step in range(1, num_steps + 1):
                await asyncio.sleep(TELEMETRY_INTERVAL_S)
                fraction = step / num_steps
                
                current_lat, current_lon, current_alt = calculate_intermediate_point(
                    start_wp.latitude, start_wp.longitude,
                    end_wp.latitude, end_wp.longitude,
                    fraction,
                    start_wp.altitude_m, end_wp.altitude_m
                )

                status_detail = "ON_SCHEDULE"
                telemetry_data = {
                    "flightId": flight_plan_with_waypoints.id,
                    "droneId": flight_plan_with_waypoints.drone_id,
                    "lat": round(current_lat, 6),
                    "lon": round(current_lon, 6),
                    "alt": round(current_alt, 2),
                    "timestamp": time.time(),
                    "status": status_detail,
                    "heading_to_waypoint_idx": i + 1
                }
                await ws_manager.broadcast_json(telemetry_data)

            current_lat, current_lon, current_alt = end_wp.latitude, end_wp.longitude, end_wp.altitude_m
            await ws_manager.broadcast_json({
                "flightId": flight_plan_with_waypoints.id,
                "droneId": flight_plan_with_waypoints.drone_id,
                "lat": current_lat, "lon": current_lon, "alt": current_alt,
                "timestamp": time.time(), "status": "WAYPOINT_REACHED", "waypoint_idx": i + 1
            })

        print(f"Flight ID {flight_plan_with_waypoints.id} simulation completed.")
        
        # Update flight status to COMPLETED using the local db session
        fp_to_complete_final = crud.get_flight_plan(db, flight_plan_with_waypoints.id) # Re-fetch to ensure attached
        if fp_to_complete_final:
            crud.update_flight_plan_status(db, flight_plan_id=fp_to_complete_final.id, status=FlightStatus.COMPLETED)
        
        await ws_manager.broadcast_json({
            "flightId": flight_plan_with_waypoints.id,
            "droneId": flight_plan_with_waypoints.drone_id,
            "status": "FLIGHT_COMPLETED",
            "timestamp": time.time()
        })

    except Exception as e:
        print(f"Error during telemetry simulation for flight {flight_plan_id}: {e}")
        db.rollback() # Rollback any pending changes in this session on error
    finally:
        db.close()