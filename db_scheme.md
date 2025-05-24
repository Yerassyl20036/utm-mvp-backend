**Database Schema Proposal - UTM MVP V1**

**Core Principles Applied:**
*   **User Model (formerly Pilot):** Central entity for authentication and ownership.
*   **Roles:** Explicit `UserRole` enum to manage permissions.
*   **Organizations:** Support for both solo users and users belonging to organizations.
*   **Soft Deletes:** `deleted_at` column for recoverable "deletions."
*   **Auditing:** `created_at` and `updated_at` timestamps on all primary tables.
*   **Data Integrity:** Use of Foreign Keys, Not Null constraints, and Unique constraints.
*   **Clarity:** Explicit naming for foreign keys and relationships.

---

**1. Table: `users`** (Formerly `pilots`)
*   Stores information about all users, regardless of role.

| Column Name                         | Data Type                        | Constraints & Notes                                     |
| :---------------------------------- | :------------------------------- | :------------------------------------------------------ |
| `id`                                | `INTEGER`                        | Primary Key, Auto-increment, Indexed                    |
| `full_name`                         | `VARCHAR(100)`                   | Not Null                                                |
| `email`                             | `VARCHAR(255)`                   | Not Null, Unique, Indexed                               |
| `phone_number`                      | `VARCHAR(20)`                    | Nullable, Unique, Indexed                               |
| `iin`                               | `VARCHAR(12)`                    | Nullable, Unique, Indexed (Kazakhstani ID)              |
| `hashed_password`                   | `VARCHAR(255)`                   | Not Null                                                |
| `role`                              | `ENUM('AUTHORITY_ADMIN', 'ORGANIZATION_ADMIN', 'ORGANIZATION_PILOT', 'SOLO_PILOT')` | Not Null |
| `organization_id`                   | `INTEGER`                        | Nullable, Foreign Key -> `organizations(id)`            |
| `is_active`                         | `BOOLEAN`                        | Not Null, Default: `TRUE`                               |
| `created_at`                        | `TIMESTAMP WITH TIME ZONE`       | Not Null, Default: `NOW()`                              |
| `updated_at`                        | `TIMESTAMP WITH TIME ZONE`       | Not Null, Default: `NOW()`, On Update: `NOW()`          |
| `deleted_at`                        | `TIMESTAMP WITH TIME ZONE`       | Nullable, Indexed (For soft delete)                     |

*Relationships:*
*   Many-to-One with `organizations` (a user can belong to one organization).
*   One-to-Many with `drones` (as `solo_owner_user`).
*   Many-to-Many with `drones` (via `user_drone_assignments`).
*   One-to-Many with `flight_plans` (as `submitter_user`).
*   One-to-Many with `flight_plans` (as `organization_approver`).
*   One-to-Many with `flight_plans` (as `authority_approver`).
*   One-to-Many with `restricted_zones` (as `creator_authority`).

---

**2. Table: `organizations`**
*   Stores information about registered organizations.

| Column Name       | Data Type                  | Constraints & Notes                                 |
| :---------------- | :------------------------- | :-------------------------------------------------- |
| `id`              | `INTEGER`                  | Primary Key, Auto-increment, Indexed                |
| `name`            | `VARCHAR(255)`             | Not Null, Unique, Indexed                           |
| `bin`             | `VARCHAR(12)`              | Not Null, Unique, Indexed (Business ID Number)      |
| `company_address` | `VARCHAR(500)`             | Not Null                                            |
| `city`            | `VARCHAR(100)`             | Not Null                                            |
| `admin_id`        | `INTEGER`                  | Nullable, Unique, Foreign Key -> `users(id)`        |
| `is_active`       | `BOOLEAN`                  | Not Null, Default: `TRUE`                           |
| `created_at`      | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`                          |
| `updated_at`      | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`, On Update: `NOW()`      |
| `deleted_at`      | `TIMESTAMP WITH TIME ZONE` | Nullable, Indexed                                   |

*Relationships:*
*   One-to-Many with `users`.
*   One-to-Many with `drones` (as `organization_owner`).
*   (Indirectly) One-to-Many with `flight_plans` (via its users/drones).

---

**3. Table: `drones`**
*   Stores information about registered drones.

| Column Name            | Data Type                               | Constraints & Notes                                    |
| :--------------------- | :-------------------------------------- | :----------------------------------------------------- |
| `id`                   | `INTEGER`                               | Primary Key, Auto-increment, Indexed                   |
| `brand`                | `VARCHAR(100)`                          | Not Null                                               |
| `model`                | `VARCHAR(100)`                          | Not Null                                               |
| `serial_number`        | `VARCHAR(100)`                          | Not Null, Unique, Indexed                              |
| `owner_type`           | `ENUM('ORGANIZATION', 'SOLO_PILOT')`    | Not Null                                               |
| `organization_id`      | `INTEGER`                               | Nullable, Foreign Key -> `organizations(id)`           |
| `solo_owner_user_id`   | `INTEGER`                               | Nullable, Foreign Key -> `users(id)`                   |
| `current_status`       | `ENUM('IDLE', 'ACTIVE', 'MAINTENANCE', 'UNKNOWN')` | Not Null, Default: `IDLE`                      |
| `last_telemetry_id`    | `BIGINTEGER`                            | Nullable, Foreign Key -> `telemetry_logs(id)` (use_alter=true for migration) |
| `last_seen_at`         | `TIMESTAMP WITH TIME ZONE`              | Nullable                                               |
| `created_at`           | `TIMESTAMP WITH TIME ZONE`              | Not Null, Default: `NOW()`                             |
| `updated_at`           | `TIMESTAMP WITH TIME ZONE`              | Not Null, Default: `NOW()`, On Update: `NOW()`         |
| `deleted_at`           | `TIMESTAMP WITH TIME ZONE`              | Nullable, Indexed                                      |

*Relationships:*
*   Many-to-One with `organizations` (if org-owned).
*   Many-to-One with `users` (if solo-owned).
*   Many-to-Many with `users` (via `user_drone_assignments`).
*   One-to-Many with `flight_plans`.
*   One-to-Many with `telemetry_logs`.
*   (Optional) One-to-One with `telemetry_logs` (for `last_telemetry_point`).

---

**4. Table: `user_drone_assignments` (M2M Join Table)**
*   Links users (Organization Pilots) to drones within an organization.

| Column Name   | Data Type                  | Constraints & Notes                        |
| :------------ | :------------------------- | :----------------------------------------- |
| `user_id`     | `INTEGER`                  | Primary Key, Foreign Key -> `users(id)`    |
| `drone_id`    | `INTEGER`                  | Primary Key, Foreign Key -> `drones(id)`   |
| `assigned_at` | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`                 |

*Relationships:*
*   Many-to-One with `users`.
*   Many-to-One with `drones`.

---

**5. Table: `flight_plans`**
*   Stores submitted flight plans.

| Column Name                             | Data Type                  | Constraints & Notes                                        |
| :-------------------------------------- | :------------------------- | :--------------------------------------------------------- |
| `id`                                    | `INTEGER`                  | Primary Key, Auto-increment, Indexed                       |
| `user_id`                               | `INTEGER`                  | Not Null, Foreign Key -> `users(id)` (Submitter)           |
| `drone_id`                              | `INTEGER`                  | Not Null, Foreign Key -> `drones(id)`                      |
| `organization_id`                       | `INTEGER`                  | Nullable, Foreign Key -> `organizations(id)`               |
| `planned_departure_time`                | `TIMESTAMP WITH TIME ZONE` | Not Null                                                   |
| `planned_arrival_time`                  | `TIMESTAMP WITH TIME ZONE` | Not Null                                                   |
| `actual_departure_time`                 | `TIMESTAMP WITH TIME ZONE` | Nullable                                                   |
| `actual_arrival_time`                   | `TIMESTAMP WITH TIME ZONE` | Nullable                                                   |
| `status`                                | `ENUM('PENDING_ORG_APPROVAL', 'PENDING_AUTHORITY_APPROVAL', 'APPROVED', 'REJECTED_BY_ORG', 'REJECTED_BY_AUTHORITY', 'ACTIVE', 'COMPLETED', 'CANCELLED_BY_PILOT', 'CANCELLED_BY_ADMIN')` | Not Null, Indexed |
| `notes`                                 | `VARCHAR(1000)`            | Nullable                                                   |
| `rejection_reason`                      | `VARCHAR(500)`             | Nullable                                                   |
| `approved_by_organization_admin_id`     | `INTEGER`                  | Nullable, Foreign Key -> `users(id)`                       |
| `approved_by_authority_admin_id`        | `INTEGER`                  | Nullable, Foreign Key -> `users(id)`                       |
| `approved_at`                           | `TIMESTAMP WITH TIME ZONE` | Nullable (Final approval time)                             |
| `created_at`                            | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`                                 |
| `updated_at`                            | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`, On Update: `NOW()`             |
| `deleted_at`                            | `TIMESTAMP WITH TIME ZONE` | Nullable, Indexed                                          |

*Relationships:*
*   Many-to-One with `users` (submitter).
*   Many-to-One with `drones`.
*   Many-to-One with `organizations` (optional).
*   Many-to-One with `users` (org approver).
*   Many-to-One with `users` (authority approver).
*   One-to-Many with `waypoints` (cascade delete).
*   One-to-Many with `telemetry_logs` (cascade delete or set null on `flight_plan_id`).

---

**6. Table: `waypoints`**
*   Stores waypoints for a flight plan (the *planned* path).

| Column Name      | Data Type | Constraints & Notes                                    |
| :--------------- | :-------- | :----------------------------------------------------- |
| `id`             | `INTEGER` | Primary Key, Auto-increment, Indexed                   |
| `flight_plan_id` | `INTEGER` | Not Null, Foreign Key -> `flight_plans(id)`, On Delete: `CASCADE`, Indexed |
| `latitude`       | `FLOAT`   | Not Null                                               |
| `longitude`      | `FLOAT`   | Not Null                                               |
| `altitude_m`     | `FLOAT`   | Not Null (e.g., AGL)                                   |
| `sequence_order` | `INTEGER` | Not Null, Indexed (Composite index with `flight_plan_id` for uniqueness) |
| `created_at`     | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`             |
| `updated_at`     | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`, On Update: `NOW()` |

*Relationships:*
*   Many-to-One with `flight_plans`.

---

**7. Table: `telemetry_logs`**
*   Stores the actual flown path and telemetry data points.

| Column Name       | Data Type                  | Constraints & Notes                                     |
| :---------------- | :------------------------- | :------------------------------------------------------ |
| `id`              | `BIGINTEGER`               | Primary Key, Auto-increment, Indexed                    |
| `flight_plan_id`  | `INTEGER`                  | Nullable (if live telemetry w/o plan), Foreign Key -> `flight_plans(id)`, On Delete: `SET NULL`, Indexed |
| `drone_id`        | `INTEGER`                  | Not Null, Foreign Key -> `drones(id)`, On Delete: `CASCADE`, Indexed |
| `timestamp`       | `TIMESTAMP WITH TIME ZONE` | Not Null, Indexed                                       |
| `latitude`        | `FLOAT`                    | Not Null                                                |
| `longitude`       | `FLOAT`                    | Not Null                                                |
| `altitude_m`      | `FLOAT`                    | Not Null                                                |
| `speed_mps`       | `FLOAT`                    | Nullable                                                |
| `heading_degrees` | `FLOAT`                    | Nullable (0-359.9)                                      |
| `status_message`  | `VARCHAR(255)`             | Nullable (e.g., "ON_SCHEDULE", "NFZ_ALERT", "SIGNAL_LOST") |
| `created_at`      | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`                              |
| `updated_at`      | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`, On Update: `NOW()`          |

*Relationships:*
*   Many-to-One with `flight_plans`.
*   Many-to-One with `drones`.

---

**8. Table: `restricted_zones` (No-Fly Zones - NFZs)**
*   Stores definitions of restricted airspace.

| Column Name                 | Data Type                  | Constraints & Notes                                      |
| :-------------------------- | :------------------------- | :------------------------------------------------------- |
| `id`                        | `INTEGER`                  | Primary Key, Auto-increment, Indexed                     |
| `name`                      | `VARCHAR(255)`             | Not Null, Indexed                                        |
| `description`               | `VARCHAR(1000)`            | Nullable                                                 |
| `geometry_type`             | `ENUM('CIRCLE', 'POLYGON')`| Not Null                                                 |
| `definition_json`           | `JSON`                     | Not Null (Stores center/radius for circle, or coordinates for polygon) |
| `min_altitude_m`            | `FLOAT`                    | Nullable                                                 |
| `max_altitude_m`            | `FLOAT`                    | Nullable                                                 |
| `is_active`                 | `BOOLEAN`                  | Not Null, Default: `TRUE`                                |
| `created_by_authority_id`   | `INTEGER`                  | Not Null, Foreign Key -> `users(id)`                     |
| `created_at`                | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`                               |
| `updated_at`                | `TIMESTAMP WITH TIME ZONE` | Not Null, Default: `NOW()`, On Update: `NOW()`           |
| `deleted_at`                | `TIMESTAMP WITH TIME ZONE` | Nullable, Indexed                                        |

*Relationships:*
*   Many-to-One with `users` (creator/authority).

---

**Summary of Enums to Define (in `app/models/` or a shared `enums.py`):**
*   `UserRole`
*   `DroneOwnerType`
*   `DroneStatus`
*   `FlightPlanStatus`
*   `NFZGeometryType`

