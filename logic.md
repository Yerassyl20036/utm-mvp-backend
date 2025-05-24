Okay, this is a significant and exciting evolution of the project requirements! The new role-based access control (RBAC) and the detailed specifications for each role, especially the Authority Admin's comprehensive view, add a lot of depth. The emphasis on map interactions and historical trajectory replay is also key.

Let's break down the **backend methodology and database design** needed to support this new, more granular system. We'll focus *only* on the backend for now, as requested.

**I. Revised Roles and Permissions - Conceptual Backend Impact**

The four roles (Authority Admin, Organization Admin, Organization Pilot, Solo Pilot) imply a more sophisticated authorization layer in the backend.

*   **Authority Admin:** Superuser. Can see and manage almost everything.
*   **Organization Admin:** Scoped admin. Manages resources (drones, pilots, flights) *within their own organization*.
*   **Organization Pilot:** User scoped to their organization. Can only manage their own flights and see assigned drones.
*   **Solo Pilot:** User not tied to an organization for flight approvals. Manages own resources, requests flights from Authority.

This will affect how we protect endpoints (`Depends` in FastAPI) and filter data in CRUD operations.

**II. Database Schema Re-evaluation & Additions**

Let's refine our existing models and add new ones based on the new requirements.

**Existing Models - Potential Modifications:**

1.  **`Organization` Model:**
    *   `id: int (PK)`
    *   `name: str (Unique, Not Null)`
    *   `bin: str (Unique, Not Null)` (Business Identification Number - from your diagram)
    *   `company_address: str (Not Null)` (From diagram)
    *   `city: str (Not Null)` (From diagram)
    *   `admin_id: int (FK to Pilot.id, Nullable)` - This will be the Organization Admin. *Initially nullable because an Org Admin registers the org first, then becomes its admin.* We'll need a process to link them.
    *   `pilots: relationship` (One-to-Many with `Pilot`)
    *   `drones: relationship` (One-to-Many with `Drone`, if orgs directly own drones, or drones are just linked via pilots)
    *   `flight_plans: relationship` (Through its pilots/drones)
    *   `is_active: bool (Default True)`
    *   `created_at: datetime`
    *   `updated_at: datetime`

2.  **`Pilot` Model:**
    *   `id: int (PK)`
    *   `full_name: str (Not Null)` (Changed from `name`, made mandatory)
    *   `email: str (Unique, Not Null)`
    *   `phone_number: str (Nullable, Unique)` (Added)
    *   `hashed_password: str (Not Null)`
    *   `role: Enum` (New field! Values: `AUTHORITY_ADMIN`, `ORGANIZATION_ADMIN`, `ORGANIZATION_PILOT`, `SOLO_PILOT`) - **CRITICAL ADDITION**
    *   `organization_id: int (FK to Organization.id, Nullable)` - Null for Solo Pilots and Authority Admins.
    *   `organization: relationship`
    *   `is_active: bool (Default True)`
    *   `is_system_admin: bool (Default False)` - This could be an alternative or supplement to `role == AUTHORITY_ADMIN`. Let's use `role` primarily.
    *   `created_at: datetime`
    *   `updated_at: datetime`
    *   `owned_drones: relationship` (Drones directly owned by this pilot if solo, or all drones if Org Admin for their org view)
    *   `assigned_drones: relationship` (Many-to-Many with `Drone` for Org Pilots - *New relationship needed*)
    *   `submitted_flight_plans: relationship` (Flights submitted by this pilot)

3.  **`Drone` Model:**
    *   `id: int (PK)`
    *   `brand: str (Not Null)` (Added)
    *   `model: str (Not Null)` (Changed from `model_name`)
    *   `serial_number: str (Unique, Not Null)`
    *   `owner_type: Enum ('ORGANIZATION', 'SOLO_PILOT')` - *NEW field to distinguish ownership*
    *   `organization_id: int (FK to Organization.id, Nullable)` - If `owner_type` is 'ORGANIZATION'.
    *   `organization: relationship`
    *   `solo_owner_pilot_id: int (FK to Pilot.id, Nullable)` - If `owner_type` is 'SOLO_PILOT'.
    *   `solo_owner_pilot: relationship`
    *   `assigned_pilots: relationship` (Many-to-Many with `Pilot` for Org Drones - *New relationship needed*)
    *   `flight_plans: relationship`
    *   `current_status: Enum ('IDLE', 'ACTIVE', 'MAINTENANCE', 'UNKNOWN')` - *NEW field for current operational status*
    *   `last_telemetry_id: int (FK to TelemetryLog.id, Nullable)` - *NEW for quick access to last known position/status.*
    *   `last_seen_at: datetime (Nullable)` - Updated by telemetry.
    *   `created_at: datetime`
    *   `updated_at: datetime`

4.  **`FlightPlan` Model:**
    *   `id: int (PK)`
    *   `pilot_id: int (FK to Pilot.id)` (Submitter)
    *   `drone_id: int (FK to Drone.id)`
    *   `organization_id: int (FK to Organization.id, Nullable)` (Organization this flight belongs to, if applicable. Helps Org Admins filter.)
    *   `planned_departure_time: datetime`
    *   `planned_arrival_time: datetime`
    *   `status: Enum(FlightStatus)` (PENDING_ORG_APPROVAL, PENDING_AUTHORITY_APPROVAL, APPROVED, REJECTED, ACTIVE, COMPLETED, CANCELLED) - *Status needs more granularity.*
    *   `rejection_reason: str (Nullable)`
    *   `approved_by_organization_admin_id: int (FK to Pilot.id, Nullable)`
    *   `approved_by_authority_admin_id: int (FK to Pilot.id, Nullable)`
    *   `approved_at: datetime (Nullable)`
    *   `actual_departure_time: datetime (Nullable)`
    *   `actual_arrival_time: datetime (Nullable)`
    *   `notes: str (Nullable)`
    *   `waypoints: relationship` (Stores the *planned* route)
    *   `telemetry_logs: relationship` (One-to-Many with `TelemetryLog` for the *actual* flown path) - **CRITICAL ADDITION**
    *   `created_at: datetime`
    *   `updated_at: datetime`

5.  **`Waypoint` Model:** (Largely unchanged, stores *planned* waypoints)
    *   `id: int (PK)`
    *   `flight_plan_id: int (FK to FlightPlan.id)`
    *   `latitude: float`
    *   `longitude: float`
    *   `altitude_m: float`
    *   `sequence_order: int`

6.  **`RestrictedZone` (NFZ) Model:**
    *   `id: int (PK)`
    *   `name: str`
    *   `geometry_type: Enum('CIRCLE', 'POLYGON')` (Or store GeoJSON directly)
    *   `definition: JSON` (e.g., `{"center_lat": ..., "radius_m": ...}` or `{"coordinates": [[[lon, lat], ...]]}`) - More flexible.
    *   `min_altitude_m: float (Nullable)`
    *   `max_altitude_m: float (Nullable)`
    *   `is_active: bool (Default True)`
    *   `created_at: datetime`
    *   `updated_at: datetime`
    *   `created_by_authority_id: int (FK to Pilot.id)` (Who defined/modified it)

**New Models Needed:**

7.  **`PilotDroneAssignment` (Association Table for Many-to-Many):**
    *   Used by Organization Admins to assign pilots to specific drones within their organization.
    *   `pilot_id: int (FK to Pilot.id, PK)`
    *   `drone_id: int (FK to Drone.id, PK)`
    *   `assigned_at: datetime`

8.  **`TelemetryLog` Model:**
    *   `id: int (PK, BigInt if high frequency)`
    *   `flight_plan_id: int (FK to FlightPlan.id)` (To link actual path to a plan)
    *   `drone_id: int (FK to Drone.id)` (For quick lookup by drone)
    *   `timestamp: datetime (timezone=True, Not Null, Indexed)`
    *   `latitude: float (Not Null)`
    *   `longitude: float (Not Null)`
    *   `altitude_m: float (Not Null)`
    *   `speed_mps: float (Nullable)`
    *   `heading_degrees: float (Nullable)`
    *   `status_message: str (Nullable)` (e.g., "ON_SCHEDULE", "NFZ_ALERT", "SIGNAL_LOST_DETECTED") - **CRITICAL for alerts**

**III. Key Backend Logic & Methodology Changes**

1.  **Registration Flow:**
    *   **Pilot Registration:**
        *   Form includes "Full Name", "Email", "Phone Number", "Password".
        *   Checkbox/Radio: "Independent Pilot" vs "Organization Member".
        *   If "Organization Member", a dropdown to select an *existing* organization (fetched from DB).
        *   On submit, `Pilot` record is created. If Org Member, `organization_id` is set. Role set to `SOLO_PILOT` or `ORGANIZATION_PILOT`.
    *   **Organization Registration (by an Organization Admin):**
        *   Separate form: "Full Name (of admin)", "Email (of admin)", "Password (for admin)", "Organization Name", "BIN", "Company Address", "City".
        *   On submit:
            1.  Create `Organization` record.
            2.  Create `Pilot` record for this org admin with `role = ORGANIZATION_ADMIN` and link `organization_id`.
            3.  Update the `Organization` record's `admin_id` with this new pilot's ID. (Requires careful transaction handling).

2.  **Authentication & Authorization (`deps.py`):**
    *   `get_current_pilot` remains largely the same (decodes JWT).
    *   New dependency functions based on `pilot.role`:
        *   `get_current_authority_admin`
        *   `get_current_organization_admin` (might also need to check they belong to the org of the resource being accessed)
        *   `get_current_organization_pilot`
        *   `get_current_solo_pilot`
    *   Permissions will be more granular. E.g., an Org Admin can only manage drones where `drone.organization_id` matches their `pilot.organization_id`.

3.  **Drone Management (`crud_drone.py`, `drones.py` endpoint):**
    *   **Adding Drones:**
        *   Solo Pilot: Sets `owner_type = 'SOLO_PILOT'`, `solo_owner_pilot_id = current_pilot.id`.
        *   Org Admin: Sets `owner_type = 'ORGANIZATION'`, `organization_id = current_pilot.organization_id`.
    *   **Pilot Assignment (Org Admin only):**
        *   New endpoint: `POST /api/v1/organizations/drones/{drone_id}/assign-pilot` with `pilot_id` in body.
        *   Creates a record in `PilotDroneAssignment`.
        *   Validation: Drone and Pilot must belong to the Org Admin's organization.
    *   Listing drones will vary based on role (own, org's, or all).

4.  **Flight Request Submission (`crud_flight.py`, `flights.py` endpoint):**
    *   **Solo Pilot:** Request `status` becomes `PENDING_AUTHORITY_APPROVAL`.
    *   **Organization Pilot:**
        *   Can only select drones assigned to them via `PilotDroneAssignment` or generally available in their org.
        *   Request `status` becomes `PENDING_ORG_APPROVAL`.
    *   The `FlightPlan` record should store the `organization_id` if submitted by an Org Pilot.

5.  **Flight Approval Workflow:**
    *   **Organization Admin (`PUT /flights/{id}/status`):**
        *   Can view flights with `status = PENDING_ORG_APPROVAL` for their `organization_id`.
        *   Can change status to `APPROVED` (which then might become `PENDING_AUTHORITY_APPROVAL` if a two-step approval is needed, or directly to `APPROVED` if orgs can self-approve certain flights - *clarify this rule*) or `REJECTED`.
        *   If approved by Org Admin and requires Authority approval, status changes to `PENDING_AUTHORITY_APPROVAL`.
    *   **Authority Admin (`PUT /flights/{id}/status`):**
        *   Can view flights with `status = PENDING_AUTHORITY_APPROVAL` (or all pending if orgs don't pre-approve).
        *   Can change status to `APPROVED` or `REJECTED`.
        *   Sets `approved_by_authority_admin_id`.

6.  **NFZ Management (Authority Admin only):**
    *   New CRUD and API endpoints (`/admin/nfz`) for creating, updating, listing, deleting `RestrictedZone` records.
    *   The `check_waypoint_against_nfzs` util will query these from the DB.

7.  **Telemetry Simulation & Logging (`telemetry_simulation.py`, `TelemetryLog` CRUD):**
    *   When a flight becomes `ACTIVE`:
        *   The simulation runs as before.
        *   **Crucially:** Each generated telemetry point (`lat`, `lon`, `alt`, `timestamp`, `speed`, `heading`, `status_message`) is **saved to the `TelemetryLog` table**, linked to the `flight_plan_id` and `drone_id`.
        *   The drone's `last_telemetry_id` and `last_seen_at` are updated.
        *   The drone's `current_status` field is updated (e.g., 'ACTIVE', 'IDLE' when flight completes).
    *   **In-flight NFZ/Violation Checks:**
        *   During simulation, for each new point, check against NFZs from the DB.
        *   If violation:
            *   Log it in `TelemetryLog` (e.g., `status_message = "NFZ_BREACH: [NFZ_NAME]"`).
            *   Broadcast this status via WebSocket.
            *   (Optional) Trigger a more formal "Alert" mechanism if we build one.
    *   **Signal Loss in Simulation:**
        *   Modify simulation to stop sending WS updates for a period.
        *   Log a "SIGNAL_LOST_SIMULATED" in `TelemetryLog` when it starts and "SIGNAL_RESTORED_SIMULATED" when it resumes.
        *   The WebSocket broadcast should reflect these statuses.

8.  **WebSocket Broadcasting (`connection_manager.py`):**
    *   The current broadcast-to-all is fine for Authority Admin to see everything.
    *   **Enhancement (if needed for Org Admin/Pilot scoped views):** The `ConnectionManager` could maintain separate lists of connections per `organization_id` or filter messages before sending if a client only wants data for their org/own flights. This requires the client to identify itself (e.g., via token on WS connect) and the manager to store this association. For MVP, broadcasting all and letting the client filter might be simpler if performance isn't an issue with few drones.
    *   **Drone Status for IDLE/LOST:**
        *   When a drone is not on an `ACTIVE` flight, its status should be `IDLE` (or `MAINTENANCE`). This info comes from the `Drone.current_status` field.
        *   For "lost connection" (yellow drones), this means no telemetry received for X time. The backend doesn't *broadcast* "I am lost." Instead, the *frontend* infers this if telemetry stops for a drone that *should* be active. The backend *can* update `Drone.current_status` to `UNKNOWN` or `SIGNAL_LOST_DB` if its simulation detects prolonged silence for a drone that it *expects* to be sending data (this is complex for a pure simulation).
        *   The simplest for "yellow drones" on the admin map is for the frontend to track last received telemetry timestamp for each active drone.
    *   **Data for Map Icons (Green, Orange, Yellow, Red):**
        *   The backend needs to provide enough information via WebSocket or a REST endpoint for the admin map to color-code:
            *   **Green (Active & On-Path):** `TelemetryLog.status_message` is "ON_SCHEDULE". `Drone.current_status` is "ACTIVE".
            *   **Orange (IDLE):** `Drone.current_status` is "IDLE". This data would need to be fetched initially for all drones and updated. *WebSocket might not be the best for idle drones unless they send a periodic "I'm idle here" message.* A REST endpoint to get all drone current states, updated periodically, might be better for idle drones. Or, a separate WS message type for drone status changes.
            *   **Yellow (Lost Connection):** Inferred by frontend if telemetry for an ACTIVE drone stops. Backend simulation can send a final "SIGNAL_LOST_SIMULATED" message.
            *   **Red (Violation):** `TelemetryLog.status_message` indicates "NFZ_BREACH" or similar.

9.  **History of Flights & Trajectory Replay:**
    *   **API Endpoint:** `GET /api/v1/flights/{flight_id}/history` (or similar).
    *   This endpoint returns the `FlightPlan` details (including *planned* `waypoints`) AND all associated `TelemetryLog` records (the *actual* flown path), ordered by timestamp.
    *   The frontend will use this data to draw both planned and actual trajectories on a map.

**IV. Database Table Relationships Summary**

*   `Organization` (1) <-> (*) `Pilot` (Org Admin, Org Pilot)
*   `Organization` (1) <-> (*) `Drone` (If orgs own drones)
*   `Pilot` (Solo) (1) <-> (*) `Drone` (If pilots own drones)
*   `PilotDroneAssignment` (Join Table): `Pilot` (*) <-> (*) `Drone` (For Org Pilots assigned to Org Drones)
*   `FlightPlan` (1) <- (*) `Waypoint` (Planned path)
*   `FlightPlan` (1) <- (*) `TelemetryLog` (Actual path)
*   `Pilot` (1) <-> (*) `FlightPlan` (Submitter)
*   `Drone` (1) <-> (*) `FlightPlan` (Aircraft used)
*   `RestrictedZone`: Standalone, checked against by flight plans.
*   `Pilot` (1) <-> (1) `Organization` (Org Admin link in Organization table)
*   `Drone` (1) -> (1) `TelemetryLog` (Link to last telemetry point for quick status)

**Next Steps for Backend Development (Iterative):**

1.  **Model & Schema Updates:** Implement all the model changes and additions. Generate and apply Alembic migrations. This is the biggest structural change.
2.  **Role-Based Auth Dependencies:** Update/create `Depends` functions in `deps.py` for the new roles.
3.  **Registration Logic:** Implement the new pilot and organization registration flows.
4.  **Drone Management (CRUD & API):** Adapt for `owner_type`, `brand`, and `PilotDroneAssignment`.
5.  **Flight Plan (CRUD & API):** Adapt for new `FlightStatus` granularity, `organization_id` linking, and multi-step approval if needed.
6.  **NFZ Management by Authority (CRUD & API for `RestrictedZone`):** And update NFZ check to use DB.
7.  **Telemetry Logging & Simulation Enhancements:** Save all telemetry to `TelemetryLog`. Add in-flight NFZ checks and signal loss simulation. Update `Drone.current_status`, `Drone.last_telemetry_id`.
8.  **History Endpoint:** Implement `/flights/{id}/history`.
9.  **Refine WebSocket Data:** Ensure broadcasts contain enough info for the frontend to color-code drones and display relevant statuses. Consider a separate message type for general drone status changes (IDLE, ACTIVE, MAINTENANCE).

This is a substantial backend refactoring and feature addition. We should tackle it piece by piece, starting with the database schema and roles, then moving to the affected CRUD operations and API endpoints.

This new plan provides a much more robust and feature-rich backend that aligns with your detailed requirements. It's a lot, so we'll need to be methodical!
