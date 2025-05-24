
**API Version Prefix:** All endpoints will be under `/api/v1/`

---

**I. Authentication Endpoints (`/auth`)**

1.  **`POST /auth/register/solo-pilot`**
    *   **Description:** Registers a new independent (solo) pilot.
    *   **Request Body:** `UserCreateSolo` (email, password, full_name, phone_number, iin)
    *   **Response Body:** `UserRead` (user details without password)
    *   **Authorization:** Public

2.  **`POST /auth/register/organization-admin`**
    *   **Description:** Registers a new organization AND its primary admin user. This is a transactional operation.
    *   **Request Body:** `OrganizationAdminRegister` (org_name, bin, company_address, city, admin_full_name, admin_email, admin_password, admin_phone_number, admin_iin)
    *   **Response Body:** `{ "organization": OrganizationRead, "admin_user": UserRead }`
    *   **Authorization:** Public

3.  **`POST /auth/register/organization-pilot`**
    *   **Description:** Registers a new pilot who will be a member of an existing organization.
    *   **Request Body:** `UserCreateOrganizationPilot` (email, password, full_name, phone_number, iin, organization_id)
    *   **Response Body:** `UserRead`
    *   **Authorization:** Public (though the organization_id provided must be valid).

4.  **`POST /auth/login/access-token`**
    *   **Description:** Logs in a user and returns a JWT access token.
    *   **Request Body:** `OAuth2PasswordRequestForm` (username=email, password)
    *   **Response Body:** `Token` (access_token, token_type)
    *   **Authorization:** Public

---

**II. User Endpoints (`/users`)**

1.  **`GET /users/me`**
    *   **Description:** Get details for the currently authenticated user.
    *   **Request Body:** None
    *   **Response Body:** `UserRead`
    *   **Authorization:** Authenticated (any role)

2.  **`PUT /users/me`**
    *   **Description:** Update details for the currently authenticated user (e.g., name, phone, password).
    *   **Request Body:** `UserUpdate` (full_name, phone_number, current_password, new_password)
    *   **Response Body:** `UserRead`
    *   **Authorization:** Authenticated (any role)

3.  **`GET /users/` (Admin Only)**
    *   **Description:** List all users in the system. Supports pagination.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`, `role: UserRole = None`, `organization_id: int = None`
    *   **Response Body:** `List[UserRead]`
    *   **Authorization:** `AUTHORITY_ADMIN`

4.  **`GET /users/{user_id}` (Admin Only)**
    *   **Description:** Get details for a specific user by ID.
    *   **Request Body:** None
    *   **Response Body:** `UserRead`
    *   **Authorization:** `AUTHORITY_ADMIN`

5.  **`PUT /users/{user_id}/status` (Admin Only)**
    *   **Description:** Activate or deactivate a user account.
    *   **Request Body:** `UserStatusUpdate` (is_active: bool)
    *   **Response Body:** `UserRead`
    *   **Authorization:** `AUTHORITY_ADMIN`

6.  **`DELETE /users/{user_id}` (Admin Only - Soft Delete)**
    *   **Description:** Soft delete a user.
    *   **Request Body:** None
    *   **Response Body:** `Status 204 No Content` or `UserRead` (of the soft-deleted user)
    *   **Authorization:** `AUTHORITY_ADMIN`

---

**III. Organization Endpoints (`/organizations`)**

1.  **`GET /organizations/`**
    *   **Description:** List all organizations. Supports pagination. (Primarily for Authority Admin, but maybe Org Admins can see their own if they somehow forgot ID - or just use `/users/me` to get their org).
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`
    *   **Response Body:** `List[OrganizationRead]`
    *   **Authorization:** `AUTHORITY_ADMIN` (Potentially authenticated users if just listing names for selection during pilot registration)

2.  **`GET /organizations/{organization_id}`**
    *   **Description:** Get details for a specific organization.
    *   **Request Body:** None
    *   **Response Body:** `OrganizationReadWithDetails` (could include list of pilots, drones, admin info)
    *   **Authorization:** `AUTHORITY_ADMIN`, or `ORGANIZATION_ADMIN` (if `organization_id` matches their org)

3.  **`PUT /organizations/{organization_id}` (Org Admin or Authority Admin)**
    *   **Description:** Update organization details.
    *   **Request Body:** `OrganizationUpdate` (name, bin, address, city, new_admin_id)
    *   **Response Body:** `OrganizationRead`
    *   **Authorization:** `AUTHORITY_ADMIN`, or `ORGANIZATION_ADMIN` (if `organization_id` matches their org, limited fields updatable by Org Admin).

4.  **`DELETE /organizations/{organization_id}` (Authority Admin Only - Soft Delete)**
    *   **Description:** Soft delete an organization. This would have cascading implications (e.g., what happens to its users, drones, flights?). For MVP, might just mark org as deleted and prevent new activity.
    *   **Request Body:** None
    *   **Response Body:** `Status 204 No Content` or `OrganizationRead`
    *   **Authorization:** `AUTHORITY_ADMIN`

5.  **`GET /organizations/{organization_id}/users` (Org Admin or Authority Admin)**
    *   **Description:** List all users belonging to a specific organization.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`
    *   **Response Body:** `List[UserRead]`
    *   **Authorization:** `AUTHORITY_ADMIN`, or `ORGANIZATION_ADMIN` (if `organization_id` matches their org)

6.  **`GET /organizations/{organization_id}/drones` (Org Admin or Authority Admin)**
    *   **Description:** List all drones belonging to a specific organization.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`
    *   **Response Body:** `List[DroneRead]`
    *   **Authorization:** `AUTHORITY_ADMIN`, or `ORGANIZATION_ADMIN` (if `organization_id` matches their org)

---

**IV. Drone Endpoints (`/drones`)**

1.  **`POST /drones/`**
    *   **Description:** Register a new drone. Ownership (`solo_owner_user_id` or `organization_id`) is determined by the authenticated user's role and input.
    *   **Request Body:** `DroneCreate` (brand, model, serial_number, [optional if org admin: organization_id])
    *   **Response Body:** `DroneRead`
    *   **Authorization:** Authenticated (`SOLO_PILOT` or `ORGANIZATION_ADMIN`)

2.  **`GET /drones/my`**
    *   **Description:** List drones relevant to the authenticated user.
        *   Solo Pilot: Lists drones where `solo_owner_user_id` matches.
        *   Org Pilot: Lists drones assigned to them via `UserDroneAssignment` within their org.
        *   Org Admin: Lists all drones within their organization.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`
    *   **Response Body:** `List[DroneRead]`
    *   **Authorization:** Authenticated (`SOLO_PILOT`, `ORGANIZATION_PILOT`, `ORGANIZATION_ADMIN`)

3.  **`GET /drones/{drone_id}`**
    *   **Description:** Get details for a specific drone.
    *   **Request Body:** None
    *   **Response Body:** `DroneRead`
    *   **Authorization:** `AUTHORITY_ADMIN`, or (`ORGANIZATION_ADMIN` / `ORGANIZATION_PILOT` / `SOLO_PILOT` if they have rights to view this drone based on ownership/assignment/organization).

4.  **`PUT /drones/{drone_id}`**
    *   **Description:** Update drone details.
    *   **Request Body:** `DroneUpdate` (brand, model, current_status). Serial number typically not updatable.
    *   **Response Body:** `DroneRead`
    *   **Authorization:** `AUTHORITY_ADMIN`, or owner (`SOLO_PILOT` or `ORGANIZATION_ADMIN` for their org's drones).

5.  **`DELETE /drones/{drone_id}` (Soft Delete)**
    *   **Description:** Soft delete a drone.
    *   **Request Body:** None
    *   **Response Body:** `Status 204 No Content` or `DroneRead`
    *   **Authorization:** `AUTHORITY_ADMIN`, or owner (`SOLO_PILOT` or `ORGANIZATION_ADMIN` for their org's drones).

6.  **`POST /drones/{drone_id}/assign-user` (Org Admin Only)**
    *   **Description:** Assign an organization pilot to a drone within the same organization.
    *   **Request Body:** `UserAssignToDrone` (user_id_to_assign)
    *   **Response Body:** `UserDroneAssignmentRead` or `Status 200 OK`
    *   **Authorization:** `ORGANIZATION_ADMIN` (must own drone and user must be in their org).

7.  **`DELETE /drones/{drone_id}/unassign-user` (Org Admin Only)**
    *   **Description:** Unassign an organization pilot from a drone.
    *   **Request Body:** `UserUnassignFromDrone` (user_id_to_unassign)
    *   **Response Body:** `Status 204 No Content`
    *   **Authorization:** `ORGANIZATION_ADMIN`

8.  **`GET /drones/admin/all` (Authority Admin Only)**
    *   **Description:** List ALL drones in the system.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`, `organization_id: int = None`, `status: DroneStatus = None`
    *   **Response Body:** `List[DroneRead]`
    *   **Authorization:** `AUTHORITY_ADMIN`

---

**V. Flight Plan Endpoints (`/flights`)**

1.  **`POST /flights/`**
    *   **Description:** Submit a new flight plan. Backend sets initial status based on submitter's role (e.g., `PENDING_ORG_APPROVAL` or `PENDING_AUTHORITY_APPROVAL`). NFZ pre-check performed.
    *   **Request Body:** `FlightPlanCreate` (drone_id, planned_departure_time, planned_arrival_time, notes, waypoints: List[WaypointCreate])
    *   **Response Body:** `FlightPlanRead`
    *   **Authorization:** Authenticated (`SOLO_PILOT`, `ORGANIZATION_PILOT`)

2.  **`GET /flights/my`**
    *   **Description:** List flight plans submitted by the currently authenticated user.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`, `status: FlightPlanStatus = None`
    *   **Response Body:** `List[FlightPlanRead]`
    *   **Authorization:** Authenticated (`SOLO_PILOT`, `ORGANIZATION_PILOT`)

3.  **`GET /flights/organization` (Org Admin Only)**
    *   **Description:** List all flight plans associated with the Organization Admin's organization.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`, `status: FlightPlanStatus = None`, `user_id: int = None` (to filter by specific pilot in their org)
    *   **Response Body:** `List[FlightPlanRead]`
    *   **Authorization:** `ORGANIZATION_ADMIN`

4.  **`GET /flights/{flight_plan_id}`**
    *   **Description:** Get details of a specific flight plan, including waypoints.
    *   **Request Body:** None
    *   **Response Body:** `FlightPlanReadWithWaypoints`
    *   **Authorization:** `AUTHORITY_ADMIN`, or submitter (`SOLO_PILOT`, `ORGANIZATION_PILOT`), or `ORGANIZATION_ADMIN` (if plan belongs to their org).

5.  **`PUT /flights/{flight_plan_id}/status`**
    *   **Description:** Update the status of a flight plan.
        *   Org Admin: Can change `PENDING_ORG_APPROVAL` to `PENDING_AUTHORITY_APPROVAL` (if two-step) or `REJECTED_BY_ORG`.
        *   Authority Admin: Can change `PENDING_AUTHORITY_APPROVAL` (or `PENDING_ORG_APPROVAL` if direct) to `APPROVED` or `REJECTED_BY_AUTHORITY`.
    *   **Request Body:** `FlightPlanStatusUpdate` (status: FlightPlanStatus, rejection_reason: Optional[str])
    *   **Response Body:** `FlightPlanRead`
    *   **Authorization:** `ORGANIZATION_ADMIN` or `AUTHORITY_ADMIN` (with logic to enforce valid state transitions).

6.  **`PUT /flights/{flight_plan_id}/start`**
    *   **Description:** Pilot starts an `APPROVED` flight. Sets status to `ACTIVE`, triggers telemetry simulation.
    *   **Request Body:** None
    *   **Response Body:** `FlightPlanRead`
    *   **Authorization:** Submitting Pilot (`SOLO_PILOT`, `ORGANIZATION_PILOT`) for their own approved plan.

7.  **`PUT /flights/{flight_plan_id}/cancel`**
    *   **Description:** Pilot or Admin cancels a flight.
        *   Pilot: Can cancel their own `PENDING` or `APPROVED` (not yet `ACTIVE`) flights. Status -> `CANCELLED_BY_PILOT`.
        *   Admin (Org/Auth): Can cancel flights in various states (e.g., `PENDING`, `APPROVED`, even `ACTIVE` for emergencies). Status -> `CANCELLED_BY_ADMIN`.
    *   **Request Body:** `FlightPlanCancel` (reason: Optional[str])
    *   **Response Body:** `FlightPlanRead`
    *   **Authorization:** Submitting Pilot, `ORGANIZATION_ADMIN`, `AUTHORITY_ADMIN` (with logic for valid states).

8.  **`GET /flights/{flight_plan_id}/history`**
    *   **Description:** Get the planned waypoints and all recorded telemetry logs for a completed or active flight.
    *   **Request Body:** None
    *   **Response Body:** `FlightPlanHistory` (flight_plan_details, planned_waypoints: List[WaypointRead], actual_telemetry: List[TelemetryLogRead])
    *   **Authorization:** `AUTHORITY_ADMIN`, submitter, relevant `ORGANIZATION_ADMIN`.

9.  **`GET /flights/admin/all` (Authority Admin Only)**
    *   **Description:** List ALL flight plans in the system.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`, `status: FlightPlanStatus = None`, `organization_id: int = None`, `user_id: int = None`
    *   **Response Body:** `List[FlightPlanRead]`
    *   **Authorization:** `AUTHORITY_ADMIN`

---

**VI. Restricted Zone (NFZ) Endpoints (`/admin/nfz`) - Authority Admin Only**

1.  **`POST /admin/nfz/`**
    *   **Description:** Create a new No-Fly Zone.
    *   **Request Body:** `RestrictedZoneCreate` (name, description, geometry_type, definition_json, min_alt, max_alt)
    *   **Response Body:** `RestrictedZoneRead`
    *   **Authorization:** `AUTHORITY_ADMIN`

2.  **`GET /admin/nfz/`**
    *   **Description:** List all No-Fly Zones.
    *   **Query Params:** `skip: int = 0`, `limit: int = 100`, `is_active: bool = None`
    *   **Response Body:** `List[RestrictedZoneRead]`
    *   **Authorization:** `AUTHORITY_ADMIN` (Possibly authenticated users for read-only to display on map during planning) - *If public read, then `GET /nfz/` without `/admin` prefix.*

3.  **`GET /nfz/` (Public or Authenticated Read for Map Display)**
    *   **Description:** List active No-Fly Zones for map display.
    *   **Response Body:** `List[RestrictedZoneRead]`
    *   **Authorization:** Public or Authenticated

4.  **`GET /admin/nfz/{zone_id}`**
    *   **Description:** Get details of a specific NFZ.
    *   **Response Body:** `RestrictedZoneRead`
    *   **Authorization:** `AUTHORITY_ADMIN`

5.  **`PUT /admin/nfz/{zone_id}`**
    *   **Description:** Update an existing NFZ.
    *   **Request Body:** `RestrictedZoneUpdate`
    *   **Response Body:** `RestrictedZoneRead`
    *   **Authorization:** `AUTHORITY_ADMIN`

6.  **`DELETE /admin/nfz/{zone_id}` (Soft Delete)**
    *   **Description:** Soft delete an NFZ.
    *   **Response Body:** `Status 204 No Content` or `RestrictedZoneRead`
    *   **Authorization:** `AUTHORITY_ADMIN`

---

**VII. Telemetry Endpoints (`/telemetry` - primarily WebSocket)**

1.  **`WS /ws/telemetry`**
    *   **Description:** WebSocket endpoint for clients to connect and receive real-time telemetry broadcasts for all active flights.
    *   **Authentication:** Token passed as query parameter (`?token=...`). Backend validates, associates connection with user if needed for future targeted messages (though MVP broadcasts all).
    *   **Messages Sent by Server:** JSON objects like `{"flightId": ..., "droneId": ..., "lat": ..., "lon": ..., "alt": ..., "timestamp": ..., "status": "ON_SCHEDULE/ALERT_NFZ/SIGNAL_LOST"}`.

---

**VIII. Additional/Utility Endpoints**

1.  **`GET /api/v1/weather` (If implemented)**
    *   **Description:** Get weather information for a given location.
    *   **Query Params:** `lat: float`, `lon: float`
    *   **Response Body:** `WeatherInfo` (temp, wind_speed, wind_direction, conditions_summary)
    *   **Authorization:** Authenticated

2.  **`GET /api/v1/remoteid/active-flights` (If implemented for Remote ID Emulation)**
    *   **Description:** Get a list of currently active flights with their emulated Remote ID data.
    *   **Response Body:** `List[RemoteIdBroadcast]` (drone_serial_number, current_lat, lon, alt, timestamp, operator_id_proxy, control_station_location_proxy)
    *   **Authorization:** Public or `AUTHORITY_ADMIN`

