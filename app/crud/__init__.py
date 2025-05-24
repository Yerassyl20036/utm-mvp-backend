# backend/app/crud/__init__.py
from .crud_pilot import get_pilot, get_pilot_by_email, get_pilots, create_pilot
from .crud_drone import ( 
    get_drone,
    get_drone_by_serial_number,
    get_drones_by_owner,
    get_all_drones,
    create_drone,
    update_drone,
    delete_drone,
    admin_delete_drone
)
from .crud_flight import ( # <--- ADD THESE
    get_flight_plan,
    get_flight_plans_by_pilot,
    get_all_flight_plans,
    create_flight_plan_with_waypoints,
    update_flight_plan_status,
    update_flight_plan,
    delete_flight_plan,
    admin_delete_flight_plan,
    create_waypoint
)
# from .crud_organization import ... # Add later