# UTM (Unmanned Traffic Management) MVP Backend

Backend service for the UTM system that manages UAV traffic, flight plans, and real-time telemetry.

## Project Overview

This project implements a FastAPI-based backend service for managing:
- Drone registrations and tracking
- Flight plans and waypoints
- Pilot and organization management
- Real-time telemetry via WebSocket
- Restricted zones and geospatial features

## Prerequisites

- Python 3.12+
- PostgreSQL
- Docker and Docker Compose (optional)

## Local Development Setup

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Environment:
- Copy `.env.example` to `.env` if it doesn't exist
- Update database credentials and other settings in `.env`

4. Database Setup:
```bash
# Create a PostgreSQL database (if not exists)
createdb utm_mvp_db

# Run database migrations
alembic upgrade head
```

5. Start the Development Server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker Setup

1. Build and start all services:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── api/            - API routes and endpoints
├── core/           - Core configurations
├── crud/           - Database operations
├── db/             - Database setup and session
├── models/         - SQLAlchemy models
├── schemas/        - Pydantic schemas
├── services/       - Business logic
├── utils/          - Utility functions
└── websockets/     - WebSocket handlers
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

## WebSocket Endpoints

The system provides real-time communication through WebSocket:
- Telemetry: `ws://localhost:8000/ws/telemetry`

## Key Features

1. **Drone Management**
   - Registration and tracking
   - Real-time telemetry monitoring

2. **Flight Planning**
   - Create and manage flight plans
   - Waypoint management
   - Collision detection

3. **User Management**
   - Pilot registration
   - Organization management
   - Authentication and authorization

4. **Safety Features**
   - Restricted zone management
   - Real-time position tracking
   - Geospatial calculations

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests
4. Submit a pull request

## Testing

Run the test suite:
```bash
pytest tests/
```