# backend/app/utils/geospatial.py
import math
from typing import List, Dict, Any, Tuple,Optional

# --- NFZ Definitions ---
# For MVP, hardcode these. In a real system, they'd come from a database or external service.
# Each NFZ can be a dictionary with 'type', 'name', and geometric properties.

# R_EARTH = 6371000  # Earth radius in meters, for more accurate distance calculations if needed

# Example: Circular NFZ (center_lat, center_lon, radius_meters)
NFZ_AIRPORT_MAIN = {
    "name": "Main City Airport NFZ",
    "type": "circle",
    "center_lat": 40.7128,  # Example: NYC
    "center_lon": -74.0060,
    "radius_m": 5000,       # 5km radius
    "min_altitude_m": 0,    # Ground level
    "max_altitude_m": 1000, # Up to 1000m (example)
    "description": "Primary airport no-fly zone."
}

# Example: Rectangular NFZ (min_lat, max_lat, min_lon, max_lon)
NFZ_GOVERNMENT_BUILDING = {
    "name": "Government Building Restricted Area",
    "type": "rectangle",
    "min_lat": 40.7500,
    "max_lat": 40.7550,
    "min_lon": -73.9900,
    "max_lon": -73.9850,
    "min_altitude_m": 0,
    "max_altitude_m": 300,
    "description": "Restricted airspace over sensitive government facility."
}

# Example: Another circular NFZ
NFZ_STADIUM_EVENT = {
    "name": "Stadium Event TFR (Temporary Flight Restriction)",
    "type": "circle",
    "center_lat": 40.6827,  # Example: Near a stadium
    "center_lon": -73.9752,
    "radius_m": 1500,       # 1.5km radius
    "min_altitude_m": 0,
    "max_altitude_m": 500,
    "description": "Temporary restriction during major events."
}


HARDCODED_NFZS: List[Dict[str, Any]] = [
    NFZ_AIRPORT_MAIN,
    NFZ_GOVERNMENT_BUILDING,
    NFZ_STADIUM_EVENT,
]

# --- Helper Functions ---

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) in meters.
    A bit overkill for small distances where planar math is fine, but good practice.
    """
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def is_point_in_circular_nfz(
    point_lat: float, point_lon: float, point_alt_m: float,
    nfz: Dict[str, Any]
) -> bool:
    """Checks if a point is within a circular NFZ, considering altitude."""
    if nfz["type"] != "circle":
        return False

    distance_to_center = haversine_distance(
        point_lat, point_lon,
        nfz["center_lat"], nfz["center_lon"]
    )
    
    # Check horizontal proximity
    if distance_to_center > nfz["radius_m"]:
        return False # Outside horizontal radius

    # Check altitude restrictions
    # Assuming point_alt_m is AGL or consistently defined with NFZ altitudes
    if nfz.get("min_altitude_m") is not None and point_alt_m < nfz["min_altitude_m"]:
        return False # Below minimum restricted altitude
    if nfz.get("max_altitude_m") is not None and point_alt_m > nfz["max_altitude_m"]:
        return False # Above maximum restricted altitude
        
    return True # Within horizontal radius and altitude constraints

def is_point_in_rectangular_nfz(
    point_lat: float, point_lon: float, point_alt_m: float,
    nfz: Dict[str, Any]
) -> bool:
    """Checks if a point is within a rectangular NFZ, considering altitude."""
    if nfz["type"] != "rectangle":
        return False

    # Check horizontal boundaries
    if not (nfz["min_lat"] <= point_lat <= nfz["max_lat"] and \
            nfz["min_lon"] <= point_lon <= nfz["max_lon"]):
        return False # Outside horizontal rectangle

    # Check altitude restrictions
    if nfz.get("min_altitude_m") is not None and point_alt_m < nfz["min_altitude_m"]:
        return False
    if nfz.get("max_altitude_m") is not None and point_alt_m > nfz["max_altitude_m"]:
        return False
            
    return True # Within horizontal rectangle and altitude constraints


# --- Main Validation Function ---
def check_waypoint_against_nfzs(
    latitude: float, longitude: float, altitude_m: float
) -> Optional[Dict[str, Any]]:
    """
    Checks a single waypoint against all hardcoded NFZs.
    Returns the NFZ object if a violation is found, otherwise None.
    """
    for nfz in HARDCODED_NFZS:
        if nfz["type"] == "circle":
            if is_point_in_circular_nfz(latitude, longitude, altitude_m, nfz):
                return nfz
        elif nfz["type"] == "rectangle":
            if is_point_in_rectangular_nfz(latitude, longitude, altitude_m, nfz):
                return nfz
    return None

# For checking an entire flight path (more complex, involves line segment intersections)
# For MVP, checking individual waypoints is a good start.
# def check_flight_path_against_nfzs(waypoints: List[Tuple[float, float, float]]) -> Optional[Dict[str, Any]]:
#     """
#     Checks an entire flight path (list of waypoints) against NFZs.
#     This is more complex as it should check segments between waypoints, not just points.
#     For MVP, we are only checking individual waypoints.
#     """
#     for i in range(len(waypoints)):
#         lat, lon, alt = waypoints[i]
#         violating_nfz = check_waypoint_against_nfzs(lat, lon, alt)
#         if violating_nfz:
#             return {"waypoint_index": i, "nfz": violating_nfz}
#
#         # TODO (Advanced): Check line segment between waypoint[i-1] and waypoint[i]
#         # This requires line-circle intersection and line-rectangle intersection algorithms.
#
#     return None