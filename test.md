Okay, this is a comprehensive request! I will generate a complete FastAPI project structure based on your `endpoints.md`, `logic.md`, and `db_scheme.md`. This will include:

1.  **Project Directory Structure:** A well-organized layout.
2.  **SQLAlchemy Models:** Based on `db_scheme.md`.
3.  **Pydantic Schemas:** For request/response validation, derived from `endpoints.md`.
4.  **API Routers and Endpoints:** Implementing all specified endpoints.
5.  **CRUD Operations:** For interacting with the database.
6.  **Authentication & Authorization:** JWT-based, with role-based access control (RBAC).
7.  **Business Logic:** Core logic from `logic.md` will be integrated.
8.  **WebSocket for Telemetry:** A basic implementation.
9.  **Alembic Migrations Setup:** For database schema management.
10. **Dockerization:** `Dockerfile` for the app and `docker-compose.yml` for the app and PostgreSQL.
11. **Configuration Management.**

Due to the sheer size of a "full implementation", the generated code will be extensive. I will provide it as a series of files that you can save into your project.

**Important Considerations & Next Steps for You:**

*   **Environment Variables:** You'll need to create a `.env` file for configuration (database URL, JWT secrets, etc.). A `.env.example` will be provided.
*   **Dependencies:** A `requirements.txt` file will be generated. You'll need to install these.
*   **Database Creation:** You'll need to ensure a PostgreSQL database is running and accessible. Docker Compose will handle this.
*   **Alembic Migrations:** You'll run `alembic revision -m "initial_migration" --autogenerate` (or similar, after reviewing the auto-generated script) and then `alembic upgrade head`.
*   **Testing:** This generated code is a strong starting point. **Thorough testing of every endpoint and logic path is crucial.**
*   **NFZ Geometry:** The NFZ `definition_json` is stored. Actual geometric intersection checks (e.g., for flight plan validation against NFZs) would typically use a geospatial library (like Shapely) or a PostGIS database extension. The provided code will include a placeholder for this logic.
*   **Telemetry Simulation:** The telemetry simulation will be basic. For a real-world scenario, this would be more complex or integrate with actual drone hardware/simulators.
*   **Error Handling & Edge Cases:** While standard error handling will be included, you may need to refine it for specific business logic edge cases.

Let's start generating the project files.

**Project Structure:**

```
.
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   ├── __init__.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── drones.py
│   │   │   ├── flights.py
│   │   │   ├── nfz.py
│   │   │   ├── organizations.py
│   │   │   ├── telemetry.py
│   │   │   ├── users.py
│   │   │   └── utility.py
│   │   └── v1.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── crud_drone.py
│   │   ├── crud_flight_plan.py
│   │   ├── crud_organization.py
│   │   ├── crud_restricted_zone.py
│   │   ├── crud_telemetry_log.py
│   │   └── crud_user.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base_class.py
│   │   ├── session.py
│   │   └── utils.py (for soft delete query helper)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── drone.py
│   │   ├── flight_plan.py
│   │   ├── organization.py
│   │   ├── restricted_zone.py
│   │   ├── telemetry_log.py
│   │   ├── user.py
│   │   └── waypoint.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── drone.py
│   │   ├── flight_plan.py
│   │   ├── msg.py
│   │   ├── organization.py
│   │   ├── restricted_zone.py
│   │   ├── telemetry.py
│   │   ├── token.py
│   │   ├── user.py
│   │   └── waypoint.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── flight_service.py
│   │   ├── nfz_service.py
│   │   └── telemetry_service.py (for simulation & WebSocket)
│   ├── __init__.py
│   └── main.py
├── .env.example
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

Now, I'll provide the content for each file.

**1. `.gitignore`**

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds Пthe exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot
*.po

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# PEP 582; __pypackages__
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak
venv.bak

# Spyder project settings
.spyderproject
.spyderworkspace

# Rope project settings
.ropeproject

# PyDev project settings
.pydevproject

# PyCharm
.idea/
*.iml
workspace.xml
tasks.xml

# VSCode
.vscode/

# alembic versions if not committed (though usually they are)
# alembic/versions/*

# Docker
docker-compose.override.yml
```

**2. `requirements.txt`**

```txt
fastapi[all]
uvicorn[standard]
sqlalchemy
psycopg2-binary
alembic
python-jose[cryptography]
passlib[bcrypt]
python-multipart  # For OAuth2PasswordRequestForm
pydantic-settings # For loading .env
greenlet # Often a dependency for SQLAlchemy async, good to have
websockets # For WebSocket support
# For NFZ geometry checks (optional, if you implement advanced checks)
# shapely
```

**3. `.env.example`**

```env
PROJECT_NAME="UTM API"
API_V1_STR="/api/v1"

# Database
POSTGRES_SERVER=db
POSTGRES_USER=utm_user
POSTGRES_PASSWORD=utm_password
POSTGRES_DB=utm_db
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}/${POSTGRES_DB}"
# For local development without Docker, you might use:
# DATABASE_URL="postgresql://utm_user:utm_password@localhost:5432/utm_db"

# JWT
SECRET_KEY=your_super_secret_key_please_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# First Superuser (Authority Admin) - used for initial setup if needed
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis
FIRST_SUPERUSER_FULL_NAME="Authority Admin"
FIRST_SUPERUSER_IIN="000000000000" # Example IIN

# WebSocket
WS_TELEMETRY_PATH="/ws/telemetry"

# For Alembic (can be the same as DATABASE_URL if app and alembic use same user/db)
# ALEMBIC_DATABASE_URL=${DATABASE_URL}
```

**4. `alembic.ini`**
(Standard Alembic config, but ensure `sqlalchemy.url` is set)

```ini
[alembic]
# path to migration scripts
script_location = alembic

# template for migration file names
# file_template = %%(rev)s_%%(slug)s

# timezone for timestamps within migration files
# timezone = UTC

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

# Alembic environment variables can be configured here
# For example, to use a different database URL for migrations:
# sqlalchemy.url = driver://user:pass@localhost/dbname
# This is often set dynamically in env.py using os.environ
```
*You will need to modify `alembic/env.py` to load `DATABASE_URL` from your settings.*

**5. `Dockerfile`**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Set environment variables to prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (if any, e.g., for psycopg2 if not using -binary)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic
COPY ./app /app/app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Uvicorn
# The --host 0.0.0.0 is important to make it accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**6. `docker-compose.yml`**

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: utm_postgres_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-utm_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-utm_password}
      POSTGRES_DB: ${POSTGRES_DB:-utm_db}
    ports:
      - "5432:5432" # Expose PostgreSQL port to host (optional, for direct access)
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-utm_user} -d ${POSTGRES_DB:-utm_db}"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: utm_fastapi_app
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app # Mount current directory to /app in container for live reload
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-utm_user}:${POSTGRES_PASSWORD:-utm_password}@db/${POSTGRES_DB:-utm_db}
      - SECRET_KEY=${SECRET_KEY:-your_super_secret_key_please_change_this_in_production}
      - ALGORITHM=${ALGORITHM:-HS256}
      - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES:-60}
      - API_V1_STR=${API_V1_STR:-/api/v1}
      - PROJECT_NAME=${PROJECT_NAME:-UTM API}
      - FIRST_SUPERUSER_EMAIL=${FIRST_SUPERUSER_EMAIL:-admin@example.com}
      - FIRST_SUPERUSER_PASSWORD=${FIRST_SUPERUSER_PASSWORD:-changethis}
      - FIRST_SUPERUSER_FULL_NAME=${FIRST_SUPERUSER_FULL_NAME:-Authority Admin}
      - FIRST_SUPERUSER_IIN=${FIRST_SUPERUSER_IIN:-000000000000}
      - WS_TELEMETRY_PATH=${WS_TELEMETRY_PATH:-/ws/telemetry}
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
```

---
Now, for the Python files within the `app` directory and `alembic` setup. This will be a lot of code. I'll provide it in chunks.

**`alembic/env.py` (Modified for settings)**

```python
from logging.config import fileConfig
import os
from dotenv import load_dotenv

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Load .env file from the project root
# Assuming env.py is in alembic/ and .env is in the parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# Import Base from your models
from app.db.base_class import Base  # Adjust if your Base is elsewhere
from app.models import * # Import all models to register them with Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    return os.getenv("DATABASE_URL")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url() # config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True, # Add this for better enum and type comparison
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration, # config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True, # Add this for better enum and type comparison
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**`app/core/config.py`**

```python
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "UTM API"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None # Will be constructed

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # First Superuser (Authority Admin)
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_FULL_NAME: str
    FIRST_SUPERUSER_IIN: str


    # WebSocket
    WS_TELEMETRY_PATH: str = "/ws/telemetry"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # This helps construct DATABASE_URL if not explicitly set
        # but it's better to set it directly in .env or docker-compose
        # For now, we assume DATABASE_URL is set directly.

settings = Settings()

# Construct DATABASE_URL if not set directly (useful if individual components are in .env)
if not settings.DATABASE_URL:
    settings.DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"

```

**`app/core/security.py`**

```python
from datetime import datetime, timedelta, timezone
from typing import Optional, Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM
JWT_SECRET_KEY = settings.SECRET_KEY


def create_access_token(subject: Any, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
```

**`app/db/base_class.py`**

```python
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime, func

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s" # e.g. User -> users

    # Default audit columns - can be overridden in specific models if needed
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, index=True)

```

**`app/db/session.py`**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**`app/db/utils.py` (for soft delete helper)**

```python
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import ColumnElement
from typing import Type, TypeVar
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)

def with_soft_delete_filter(query: Query, model: Type[ModelType], include_deleted: bool = False) -> Query:
    """Applies a filter to exclude soft-deleted records unless include_deleted is True."""
    if not include_deleted and hasattr(model, 'deleted_at'):
        return query.filter(model.deleted_at.is_(None))
    return query

def get_active_query(db: Session, model: Type[ModelType]) -> Query:
    """Returns a query for the model that filters out soft-deleted records."""
    if hasattr(model, 'deleted_at'):
        return db.query(model).filter(model.deleted_at.is_(None))
    return db.query(model) # If model doesn't have deleted_at, return normal query

def apply_soft_delete_filter_to_query_condition(model: Type[ModelType], condition: ColumnElement) -> ColumnElement:
    """Combines a given condition with the soft delete filter."""
    if hasattr(model, 'deleted_at'):
        return (condition) & (model.deleted_at.is_(None))
    return condition
```

---
Next, the models (`app/models/`). I'll create one file per table as per the structure.

**`app/models/__init__.py`**

```python
from .user import User, UserRole  # UserRole enum needs to be accessible
from .organization import Organization
from .drone import Drone, DroneOwnerType, DroneStatus # Enums
from .user_drone_assignment import UserDroneAssignment
from .flight_plan import FlightPlan, FlightPlanStatus # Enum
from .waypoint import Waypoint
from .telemetry_log import TelemetryLog
from .restricted_zone import RestrictedZone, NFZGeometryType # Enum

# This helps Alembic find all models
from app.db.base_class import Base
```

**`app/models/user.py`**

```python
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    AUTHORITY_ADMIN = "AUTHORITY_ADMIN"
    ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN"
    ORGANIZATION_PILOT = "ORGANIZATION_PILOT"
    SOLO_PILOT = "SOLO_PILOT"

class User(Base):
    __tablename__ = "users" # Explicitly set as per db_scheme.md

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=True)
    iin = Column(String(12), unique=True, index=True, nullable=True) # Kazakhstani ID
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", name="fk_user_organization_id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    # created_at, updated_at, deleted_at from Base

    # Relationships
    organization = relationship("Organization", back_populates="users", foreign_keys=[organization_id])
    
    # Drones owned by solo pilot
    owned_drones_solo = relationship(
        "Drone",
        foreign_keys="[Drone.solo_owner_user_id]",
        back_populates="solo_owner_user",
        lazy="selectin" # Or "joined" if frequently accessed
    )
    
    # Drones assigned to this user (M2M)
    assigned_drones_through_link = relationship("UserDroneAssignment", back_populates="user", lazy="selectin")

    submitted_flight_plans = relationship("FlightPlan", foreign_keys="[FlightPlan.user_id]", back_populates="submitter_user", lazy="selectin")
    
    # For flight plan approvals
    organization_approved_flight_plans = relationship(
        "FlightPlan",
        foreign_keys="[FlightPlan.approved_by_organization_admin_id]",
        back_populates="organization_approver",
        lazy="selectin"
    )
    authority_approved_flight_plans = relationship(
        "FlightPlan",
        foreign_keys="[FlightPlan.approved_by_authority_admin_id]",
        back_populates="authority_approver",
        lazy="selectin"
    )
    
    created_restricted_zones = relationship(
        "RestrictedZone",
        foreign_keys="[RestrictedZone.created_by_authority_id]",
        back_populates="creator_authority",
        lazy="selectin"
    )

    # For organization admin link
    # If an organization has one admin, this relationship is on the Organization model
    # admin_of_organization = relationship("Organization", back_populates="admin_user", uselist=False)
```

**`app/models/organization.py`**

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    bin = Column(String(12), unique=True, index=True, nullable=False) # Business ID Number
    company_address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id", name="fk_organization_admin_id"), unique=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    # created_at, updated_at, deleted_at from Base

    # Relationships
    users = relationship("User", back_populates="organization", foreign_keys="[User.organization_id]")
    admin_user = relationship("User", foreign_keys=[admin_id]) # , back_populates="admin_of_organization"
    
    # Drones owned by this organization
    owned_drones = relationship(
        "Drone",
        foreign_keys="[Drone.organization_id]",
        back_populates="organization_owner",
        lazy="selectin"
    )

    # Flight plans related to this organization (indirectly via users or drones)
    # This can be complex to model directly if not explicitly linked.
    # We can query flight plans where flight_plan.organization_id is set.
    flight_plans = relationship("FlightPlan", back_populates="organization", foreign_keys="[FlightPlan.organization_id]")
```

**`app/models/drone.py`**

```python
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SAEnum, BigInteger
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class DroneOwnerType(str, enum.Enum):
    ORGANIZATION = "ORGANIZATION"
    SOLO_PILOT = "SOLO_PILOT"

class DroneStatus(str, enum.Enum):
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"
    MAINTENANCE = "MAINTENANCE"
    UNKNOWN = "UNKNOWN"

class Drone(Base):
    __tablename__ = "drones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True, index=True, nullable=False)
    owner_type = Column(SAEnum(DroneOwnerType), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", name="fk_drone_organization_id"), nullable=True)
    solo_owner_user_id = Column(Integer, ForeignKey("users.id", name="fk_drone_solo_owner_user_id"), nullable=True)
    current_status = Column(SAEnum(DroneStatus), nullable=False, default=DroneStatus.IDLE)
    # last_telemetry_id: Foreign key to telemetry_logs. Needs careful handling with Alembic if telemetry_logs table is defined later.
    # Alembic use_alter=True helps here.
    last_telemetry_id = Column(BigInteger, ForeignKey("telemetry_logs.id", name="fk_drone_last_telemetry_id", use_alter=True), nullable=True)
    last_seen_at = Column(DateTime(timezone=True), nullable=True)
    # created_at, updated_at, deleted_at from Base

    # Relationships
    organization_owner = relationship("Organization", back_populates="owned_drones", foreign_keys=[organization_id])
    solo_owner_user = relationship("User", back_populates="owned_drones_solo", foreign_keys=[solo_owner_user_id])
    
    # Users assigned to this drone (M2M)
    assigned_users_through_link = relationship("UserDroneAssignment", back_populates="drone", lazy="selectin")

    flight_plans = relationship("FlightPlan", back_populates="drone", lazy="selectin")
    telemetry_logs = relationship("TelemetryLog", back_populates="drone", foreign_keys="[TelemetryLog.drone_id]", lazy="selectin") # All logs for this drone

    # Relationship for last_telemetry_id if you want to load the object
    # last_telemetry_point = relationship("TelemetryLog", foreign_keys=[last_telemetry_id])
```

**`app/models/user_drone_assignment.py`**

```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base # Or just from sqlalchemy.ext.declarative import declarative_base; Base = declarative_base() if no common base

# This is an association table, so it might not need created_at, updated_at, deleted_at from the common Base
# if it's purely for linking. However, assigned_at is useful.
# For simplicity and consistency with db_scheme.md, let's assume it doesn't inherit Base
# but defines its own columns. If it needs soft delete or audit, it should inherit Base.
# The db_scheme.md does not show created_at/updated_at for this table.

class UserDroneAssignment(Base): # Changed to inherit Base for consistency and potential future needs
    __tablename__ = "user_drone_assignments"
    # No separate 'id' column, using composite PK

    user_id = Column(Integer, ForeignKey("users.id", name="fk_user_drone_assignment_user_id", ondelete="CASCADE"), primary_key=True)
    drone_id = Column(Integer, ForeignKey("drones.id", name="fk_user_drone_assignment_drone_id", ondelete="CASCADE"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    # __table_args__ = (PrimaryKeyConstraint('user_id', 'drone_id'),) # Already defined by primary_key=True on columns

    # Relationships
    user = relationship("User", back_populates="assigned_drones_through_link")
    drone = relationship("Drone", back_populates="assigned_users_through_link")

    # Remove Base's default id, created_at, updated_at, deleted_at if not needed.
    # Overriding them to be None or not present if this table is purely structural.
    # For this specific table, `id` `deleted_at` might not be applicable.
    # `created_at` is `assigned_at`. `updated_at` could be useful if assignments can be modified.
    # Let's remove the Base's id, and keep assigned_at as created_at.
    # If we don't inherit Base, define columns manually.
    # For now, inheriting Base and `assigned_at` acts as `created_at`. `updated_at` is fine. `id` and `deleted_at` might be unused.
    # To match db_scheme.md strictly, it would not inherit Base and only have user_id, drone_id, assigned_at.
    # Let's make it inherit Base for now, and assigned_at is the specific timestamp.
    # We can choose to ignore Base.id for this table in queries if we always use composite PK.
    # Overriding Base columns:
    id = None # type: ignore
    deleted_at = None # type: ignore
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), name="assigned_at_proxy") # Proxy to use assigned_at as created_at
    # Actual assigned_at is already defined.
```
*Self-correction: The `UserDroneAssignment` table in `db_scheme.md` has `assigned_at` but not the standard audit columns. It also uses a composite primary key. Let's adjust to match that more closely by not inheriting `Base` or carefully overriding.*

**Corrected `app/models/user_drone_assignment.py`** (Not inheriting `Base` for this specific M2M table as per `db_scheme.md` structure)

```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Using a local Base for this specific table if it doesn't fit the common Base pattern
LocalBase = declarative_base()

class UserDroneAssignment(LocalBase):
    __tablename__ = "user_drone_assignments"

    user_id = Column(Integer, ForeignKey("users.id", name="fk_user_drone_assignment_user_id", ondelete="CASCADE"), primary_key=True)
    drone_id = Column(Integer, ForeignKey("drones.id", name="fk_user_drone_assignment_drone_id", ondelete="CASCADE"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    __table_args__ = (PrimaryKeyConstraint('user_id', 'drone_id', name='pk_user_drone_assignment'),)

    # Relationships
    # These need to be defined where User and Drone models are, or use backref string.
    # For clarity, we'll assume User and Drone models will have:
    # user = relationship("User", back_populates="drone_assignments")
    # drone = relationship("Drone", back_populates="user_assignments")
    # The current User and Drone models use `assigned_drones_through_link` and `assigned_users_through_link`
    # which point to this UserDroneAssignment model. So, this side of relationship is:
    user = relationship("User", back_populates="assigned_drones_through_link")
    drone = relationship("Drone", back_populates="assigned_users_through_link")

```
*Re-correction: Let's stick to inheriting `Base` for all tables for consistency in `Base.metadata.create_all()` and Alembic, and just be mindful of the primary key for `UserDroneAssignment`. The `id` from `Base` can be ignored for this table if composite PK is always used.*

**Re-corrected `app/models/user_drone_assignment.py` (Inheriting Base, but PK is composite)**

```python
from sqlalchemy import Column, Integer, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class UserDroneAssignment(Base):
    __tablename__ = "user_drone_assignments"

    # Override the 'id' from Base as it's not the PK here.
    # We'll use a composite primary key.
    # The 'id' column from Base will still exist but won't be the PK.
    # This is a common pattern if you want audit columns on an association table.
    # Alternatively, don't inherit Base if you strictly want only the M2M columns.
    # For now, let's keep Base inheritance for potential audit consistency.

    user_id = Column(Integer, ForeignKey("users.id", name="fk_user_drone_assignment_user_id", ondelete="CASCADE"), primary_key=True)
    drone_id = Column(Integer, ForeignKey("drones.id", name="fk_user_drone_assignment_drone_id", ondelete="CASCADE"), primary_key=True)
    
    # 'created_at' from Base can serve as 'assigned_at' if default=func.now() is acceptable.
    # If a distinct 'assigned_at' is needed separate from 'created_at', define it:
    # assigned_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    # For simplicity, let's assume Base.created_at IS assigned_at for this table.
    # The db_scheme.md explicitly lists `assigned_at`. So let's add it and make Base.created_at distinct or unused.

    # To match db_scheme.md which has `assigned_at` and no other audit columns for this table:
    # We should NOT inherit Base.
    # Let's go with the previous correction: Not inheriting Base for this specific table.
    # This means it won't have `created_at`, `updated_at`, `deleted_at` from the common Base.
    # This is the cleanest way to match the provided db_scheme.md for this specific table.
    # So, the "Corrected app/models/user_drone_assignment.py" (the one NOT inheriting Base) is better.
    # I will proceed with that version.

    # Reverting to the non-Base inheriting version for UserDroneAssignment for strict schema adherence.
    # This means UserDroneAssignment will NOT be in Base.metadata automatically unless explicitly added.
    # This is a slight complication for Alembic if `target_metadata = Base.metadata` is used.
    # A common practice is to have all tables inherit from the same Base.
    # Let's make a pragmatic choice: inherit Base, and `assigned_at` is the primary timestamp.
    # The `id` from Base will be there but not the primary key.
    
    # Final decision for UserDroneAssignment: Inherit Base, `created_at` from Base IS `assigned_at`.
    # This keeps all tables under one Base.metadata for Alembic.
    # The `db_scheme.md` `assigned_at` will map to `Base.created_at`.
    # The `id` column from `Base` will exist but `user_id, drone_id` will be the composite PK.

    # Override 'id' from Base as it's not the PK here.
    # The 'id' column from Base will still exist.
    # This is a bit of a compromise to keep all models under one Base.
    # The primary key constraint will ensure uniqueness.
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'drone_id', name='pk_user_drone_assignment'),
        {}, # Ensure this is a tuple for other args like schema
    )
    # `created_at` from Base will serve as `assigned_at`.
    # `updated_at` and `deleted_at` from Base are available if needed.
    # `id` from Base is also available, though not the PK.

    # Relationships
    user = relationship("User", back_populates="assigned_drones_through_link")
    drone = relationship("Drone", back_populates="assigned_users_through_link")
```

**`app/models/flight_plan.py`**

```python
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class FlightPlanStatus(str, enum.Enum):
    PENDING_ORG_APPROVAL = "PENDING_ORG_APPROVAL"
    PENDING_AUTHORITY_APPROVAL = "PENDING_AUTHORITY_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED_BY_ORG = "REJECTED_BY_ORG"
    REJECTED_BY_AUTHORITY = "REJECTED_BY_AUTHORITY"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED_BY_PILOT = "CANCELLED_BY_PILOT"
    CANCELLED_BY_ADMIN = "CANCELLED_BY_ADMIN"

class FlightPlan(Base):
    __tablename__ = "flight_plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", name="fk_flight_plan_user_id"), nullable=False) # Submitter
    drone_id = Column(Integer, ForeignKey("drones.id", name="fk_flight_plan_drone_id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", name="fk_flight_plan_organization_id"), nullable=True)
    
    planned_departure_time = Column(DateTime(timezone=True), nullable=False)
    planned_arrival_time = Column(DateTime(timezone=True), nullable=False)
    actual_departure_time = Column(DateTime(timezone=True), nullable=True)
    actual_arrival_time = Column(DateTime(timezone=True), nullable=True)
    
    status = Column(SAEnum(FlightPlanStatus), nullable=False, index=True)
    notes = Column(Text, nullable=True) # VARCHAR(1000) in schema, Text is more flexible
    rejection_reason = Column(String(500), nullable=True)
    
    approved_by_organization_admin_id = Column(Integer, ForeignKey("users.id", name="fk_flight_plan_org_admin_id"), nullable=True)
    approved_by_authority_admin_id = Column(Integer, ForeignKey("users.id", name="fk_flight_plan_auth_admin_id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True) # Final approval time
    # created_at, updated_at, deleted_at from Base

    # Relationships
    submitter_user = relationship("User", foreign_keys=[user_id], back_populates="submitted_flight_plans")
    drone = relationship("Drone", back_populates="flight_plans")
    organization = relationship("Organization", back_populates="flight_plans", foreign_keys=[organization_id])
    
    organization_approver = relationship("User", foreign_keys=[approved_by_organization_admin_id], back_populates="organization_approved_flight_plans")
    authority_approver = relationship("User", foreign_keys=[approved_by_authority_admin_id], back_populates="authority_approved_flight_plans")
    
    waypoints = relationship("Waypoint", back_populates="flight_plan", cascade="all, delete-orphan", lazy="selectin")
    telemetry_logs = relationship("TelemetryLog", back_populates="flight_plan", cascade="all, delete-orphan", lazy="selectin") # Or set null on delete
```

**`app/models/waypoint.py`**

```python
from sqlalchemy import Column, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Waypoint(Base):
    __tablename__ = "waypoints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    flight_plan_id = Column(Integer, ForeignKey("flight_plans.id", name="fk_waypoint_flight_plan_id", ondelete="CASCADE"), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_m = Column(Float, nullable=False) # AGL
    sequence_order = Column(Integer, nullable=False)
    # created_at, updated_at from Base. deleted_at might not be relevant if waypoints are immutable once plan is set.

    # Relationships
    flight_plan = relationship("FlightPlan", back_populates="waypoints")

    __table_args__ = (
        Index("ix_waypoint_flight_plan_id_sequence_order", "flight_plan_id", "sequence_order", unique=True),
    )
```

**`app/models/telemetry_log.py`**

```python
from sqlalchemy import Column, BigInteger, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    # flight_plan_id can be nullable if live telemetry w/o plan, but for this project, assume it's linked.
    # Or, as per schema, ondelete SET NULL if a flight plan is deleted but logs are kept.
    flight_plan_id = Column(Integer, ForeignKey("flight_plans.id", name="fk_telemetry_log_flight_plan_id", ondelete="SET NULL"), nullable=True, index=True)
    drone_id = Column(Integer, ForeignKey("drones.id", name="fk_telemetry_log_drone_id", ondelete="CASCADE"), nullable=False, index=True)
    
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_m = Column(Float, nullable=False)
    speed_mps = Column(Float, nullable=True)
    heading_degrees = Column(Float, nullable=True) # 0-359.9
    status_message = Column(String(255), nullable=True) # e.g., "ON_SCHEDULE", "NFZ_ALERT"
    # created_at, updated_at from Base. deleted_at might not be relevant for telemetry.

    # Relationships
    flight_plan = relationship("FlightPlan", back_populates="telemetry_logs")
    drone = relationship("Drone", back_populates="telemetry_logs", foreign_keys=[drone_id])
```

**`app/models/restricted_zone.py`**

```python
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SAEnum, Float, JSON, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class NFZGeometryType(str, enum.Enum):
    CIRCLE = "CIRCLE"
    POLYGON = "POLYGON"

class RestrictedZone(Base):
    __tablename__ = "restricted_zones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True) # VARCHAR(1000) in schema
    geometry_type = Column(SAEnum(NFZGeometryType), nullable=False)
    definition_json = Column(JSON, nullable=False) # Stores center/radius for circle, or coordinates for polygon
    min_altitude_m = Column(Float, nullable=True)
    max_altitude_m = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_by_authority_id = Column(Integer, ForeignKey("users.id", name="fk_restricted_zone_creator_id"), nullable=False)
    # created_at, updated_at, deleted_at from Base

    # Relationships
    creator_authority = relationship("User", back_populates="created_restricted_zones", foreign_keys=[created_by_authority_id])
```

---
This covers the models. Next are Pydantic Schemas (`app/schemas/`). This will also be extensive.

I will continue in the next response with Schemas, CRUD, API deps, Routers, Services, and `main.py`.
This is a very large code generation task. I'll do my best to make it coherent and functional as a starting point.
Please ensure you have a way to save these code blocks into the correct files in the project structure I outlined.
The next part will be Schemas.Okay, continuing with the Pydantic Schemas, CRUD operations, API dependencies, Routers, Services, and finally `main.py`.

**`app/schemas/__init__.py`**

```python
from .token import Token, TokenPayload
from .msg import Msg

from .user import (
    UserBase,
    UserCreateSolo,
    UserCreateOrganizationPilot,
    UserCreate, # Generic internal create
    UserUpdate,
    UserRead,
    UserRole, # Re-export enum for API use
    UserStatusUpdate,
    OrganizationAdminRegister,
    OrganizationAdminRegisterResponse,
)
from .organization import (
    OrganizationBase,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationRead,
    OrganizationReadWithDetails, # Placeholder, can extend OrganizationRead
)
from .drone import (
    DroneBase,
    DroneCreate,
    DroneUpdate,
    DroneRead,
    DroneOwnerType, # Re-export
    DroneStatus,    # Re-export
    UserAssignToDrone,
    UserUnassignFromDrone,
    UserDroneAssignmentRead, # For response of assignment
)
from .waypoint import (
    WaypointBase,
    WaypointCreate,
    WaypointRead,
    WaypointUpdate, # If needed
)
from .flight_plan import (
    FlightPlanBase,
    FlightPlanCreate,
    FlightPlanUpdate, # If needed for general updates by pilot
    FlightPlanRead,
    FlightPlanReadWithWaypoints,
    FlightPlanStatus, # Re-export
    FlightPlanStatusUpdate,
    FlightPlanCancel,
    FlightPlanHistory,
)
from .telemetry import (
    TelemetryLogBase,
    TelemetryLogCreate,
    TelemetryLogRead,
    LiveTelemetryMessage, # For WebSocket
)
from .restricted_zone import (
    RestrictedZoneBase,
    RestrictedZoneCreate,
    RestrictedZoneUpdate,
    RestrictedZoneRead,
    NFZGeometryType, # Re-export
)
from .utility import (
    WeatherInfo,
    RemoteIdBroadcast,
)
```

**`app/schemas/token.py`**

```python
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
```

**`app/schemas/msg.py`**

```python
from pydantic import BaseModel

class Msg(BaseModel):
    message: str
```

**`app/schemas/user.py`**

```python
from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole # Import the enum from models

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[constr(max_length=20)] = None
    iin: Optional[constr(min_length=12, max_length=12)] = None # Kazakhstani IIN

# Properties to receive via API on creation (generic)
class UserCreate(UserBase):
    password: str
    role: UserRole # Role must be specified on creation

# Properties for Solo Pilot Registration
class UserCreateSolo(UserBase):
    password: str

# Properties for Organization Pilot Registration
class UserCreateOrganizationPilot(UserBase):
    password: str
    organization_id: int

# Properties for Organization Admin Registration (part of OrganizationAdminRegister)
class AdminUserCreateForOrg(UserBase):
    password: str # Renamed from admin_password for consistency

# Properties to receive via API on update
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[constr(max_length=20)] = None
    current_password: Optional[str] = None # Required if changing password
    new_password: Optional[str] = None

# Properties to return to client
class UserRead(UserBase):
    id: int
    role: UserRole
    is_active: bool
    organization_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# For registering an organization and its admin
class OrganizationAdminRegister(BaseModel):
    org_name: str
    bin: constr(min_length=12, max_length=12)
    company_address: str
    city: str
    admin_full_name: str
    admin_email: EmailStr
    admin_password: str
    admin_phone_number: Optional[constr(max_length=20)] = None
    admin_iin: Optional[constr(min_length=12, max_length=12)] = None

class OrganizationAdminRegisterResponse(BaseModel):
    organization: "OrganizationRead" # Forward reference
    admin_user: UserRead

class UserStatusUpdate(BaseModel):
    is_active: bool
```

**`app/schemas/organization.py`**

```python
from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime
from app.schemas.user import UserRead # For admin_user and users list

# Shared properties
class OrganizationBase(BaseModel):
    name: str
    bin: constr(min_length=12, max_length=12)
    company_address: str
    city: str

# Properties to receive via API on creation (handled by /auth/register/organization-admin)
# class OrganizationCreate(OrganizationBase):
#     admin_id: Optional[int] = None # Set after admin user is created

# Properties to receive via API on update
class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    bin: Optional[constr(min_length=12, max_length=12)] = None
    company_address: Optional[str] = None
    city: Optional[str] = None
    new_admin_id: Optional[int] = None # To change the organization admin

# Properties to return to client
class OrganizationRead(OrganizationBase):
    id: int
    admin_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # admin_user: Optional[UserRead] = None # Can be added if needed

    class Config:
        from_attributes = True

class OrganizationReadWithDetails(OrganizationRead):
    # users: List[UserRead] = [] # Example: list of pilots
    # drones: List["DroneRead"] = [] # Example: list of drones
    admin_user: Optional[UserRead] = None
    # Add more details as needed based on endpoint III.2
    pass

# For OrganizationAdminRegisterResponse to resolve forward reference
from app.schemas.user import UserRead
OrganizationAdminRegisterResponse.model_rebuild()
```

**`app/schemas/drone.py`**

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.drone import DroneOwnerType, DroneStatus # Import enums

# Shared properties
class DroneBase(BaseModel):
    brand: str
    model: str
    serial_number: str

# Properties to receive via API on creation
class DroneCreate(DroneBase):
    # Ownership is determined by authenticated user's role and this optional field
    organization_id: Optional[int] = None # If Org Admin registers for their org

# Properties to receive via API on update
class DroneUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    # serial_number: Optional[str] = None # Typically not updatable
    current_status: Optional[DroneStatus] = None

# Properties to return to client
class DroneRead(DroneBase):
    id: int
    owner_type: DroneOwnerType
    organization_id: Optional[int] = None
    solo_owner_user_id: Optional[int] = None
    current_status: DroneStatus
    last_seen_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserAssignToDrone(BaseModel):
    user_id_to_assign: int

class UserUnassignFromDrone(BaseModel):
    user_id_to_unassign: int

class UserDroneAssignmentRead(BaseModel):
    user_id: int
    drone_id: int
    assigned_at: datetime # This comes from Base.created_at in our model compromise

    class Config:
        from_attributes = True
```

**`app/schemas/waypoint.py`**

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Shared properties
class WaypointBase(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude_m: float = Field(..., gt=0) # Altitude above ground level
    sequence_order: int = Field(..., ge=0)

# Properties to receive via API on creation
class WaypointCreate(WaypointBase):
    pass

# Properties to receive via API on update (if waypoints are updatable post-creation)
class WaypointUpdate(WaypointBase):
    pass

# Properties to return to client
class WaypointRead(WaypointBase):
    id: int
    flight_plan_id: int
    # created_at: datetime # from Base, if needed
    # updated_at: datetime # from Base, if needed

    class Config:
        from_attributes = True
```

**`app/schemas/flight_plan.py`**

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.flight_plan import FlightPlanStatus # Import enum
from app.schemas.waypoint import WaypointCreate, WaypointRead
from app.schemas.drone import DroneRead
from app.schemas.user import UserRead
from app.schemas.telemetry import TelemetryLogRead # Forward reference

# Shared properties
class FlightPlanBase(BaseModel):
    drone_id: int
    planned_departure_time: datetime
    planned_arrival_time: datetime
    notes: Optional[str] = None

# Properties to receive via API on creation
class FlightPlanCreate(FlightPlanBase):
    waypoints: List[WaypointCreate]

# Properties to receive via API on update (e.g., by pilot before approval)
# This is not explicitly in endpoints.md but could be useful
class FlightPlanUpdate(BaseModel):
    planned_departure_time: Optional[datetime] = None
    planned_arrival_time: Optional[datetime] = None
    notes: Optional[str] = None
    waypoints: Optional[List[WaypointCreate]] = None # Allow updating waypoints before approval

# Properties to return to client
class FlightPlanRead(FlightPlanBase):
    id: int
    user_id: int # Submitter
    organization_id: Optional[int] = None
    status: FlightPlanStatus
    actual_departure_time: Optional[datetime] = None
    actual_arrival_time: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    approved_by_organization_admin_id: Optional[int] = None
    approved_by_authority_admin_id: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    # drone: Optional[DroneRead] = None # Can be added for richer response
    # submitter_user: Optional[UserRead] = None # Can be added

    class Config:
        from_attributes = True

class FlightPlanReadWithWaypoints(FlightPlanRead):
    waypoints: List[WaypointRead] = []
    drone: Optional[DroneRead] = None # Example of richer data
    submitter_user: Optional[UserRead] = None # Example

class FlightPlanStatusUpdate(BaseModel):
    status: FlightPlanStatus
    rejection_reason: Optional[str] = None

class FlightPlanCancel(BaseModel):
    reason: Optional[str] = None

class FlightPlanHistory(BaseModel):
    flight_plan_details: FlightPlanReadWithWaypoints
    # planned_waypoints: List[WaypointRead] # Already in FlightPlanReadWithWaypoints
    actual_telemetry: List["TelemetryLogRead"] # Forward reference

# Resolve forward reference
FlightPlanHistory.model_rebuild()
```

**`app/schemas/telemetry.py`**

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Shared properties for DB log
class TelemetryLogBase(BaseModel):
    timestamp: datetime
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude_m: float
    speed_mps: Optional[float] = Field(default=None, ge=0)
    heading_degrees: Optional[float] = Field(default=None, ge=0, le=360)
    status_message: Optional[str] = None

# Properties to receive for creating a log entry (usually internal)
class TelemetryLogCreate(TelemetryLogBase):
    flight_plan_id: Optional[int] = None # Can be null if not tied to a plan initially
    drone_id: int

# Properties to return to client for a log entry
class TelemetryLogRead(TelemetryLogBase):
    id: int # BigInt in DB, int here is fine for Pydantic
    flight_plan_id: Optional[int] = None
    drone_id: int
    created_at: datetime # from Base

    class Config:
        from_attributes = True

# Message format for WebSocket broadcast
class LiveTelemetryMessage(BaseModel):
    flight_id: int # flight_plan_id
    drone_id: int
    lat: float
    lon: float
    alt: float # altitude_m
    timestamp: datetime
    speed: Optional[float] = None # speed_mps
    heading: Optional[float] = None # heading_degrees
    # status: str # e.g., "ON_SCHEDULE/ALERT_NFZ/SIGNAL_LOST" -> from TelemetryLog.status_message
    status_message: Optional[str] = None
```
*Self-correction: The `flight_plan_id` in `TelemetryLogCreate` should be `Optional[int]` as per the DB schema (`Nullable`).*

**`app/schemas/restricted_zone.py`**

```python
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime
from app.models.restricted_zone import NFZGeometryType # Import enum

# Shared properties
class RestrictedZoneBase(BaseModel):
    name: str
    description: Optional[str] = None
    geometry_type: NFZGeometryType
    definition_json: Dict[str, Any] # e.g., {"center_lat": ..., "radius_m": ...} or {"coordinates": ...}
    min_altitude_m: Optional[float] = Field(default=None, ge=0)
    max_altitude_m: Optional[float] = Field(default=None, ge=0) # Could be validated against min_alt

# Properties to receive via API on creation
class RestrictedZoneCreate(RestrictedZoneBase):
    pass

# Properties to receive via API on update
class RestrictedZoneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    geometry_type: Optional[NFZGeometryType] = None
    definition_json: Optional[Dict[str, Any]] = None
    min_altitude_m: Optional[float] = None
    max_altitude_m: Optional[float] = None
    is_active: Optional[bool] = None

# Properties to return to client
class RestrictedZoneRead(RestrictedZoneBase):
    id: int
    is_active: bool
    created_by_authority_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**`app/schemas/utility.py`**

```python
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WeatherInfo(BaseModel):
    # Example fields, adjust based on actual weather API response
    lat: float
    lon: float
    temp: float # Celsius
    wind_speed: float # m/s
    wind_direction: float # degrees
    conditions_summary: str
    timestamp: datetime

class RemoteIdBroadcast(BaseModel):
    drone_serial_number: str
    current_lat: float
    current_lon: float # Corrected from lon
    current_alt: float # Corrected from alt
    timestamp: datetime
    operator_id_proxy: Optional[str] = None # e.g., masked user ID or org ID
    control_station_location_proxy: Optional[Dict[str, float]] = None # e.g., {"lat": ..., "lon": ...}
```

---
Next, CRUD operations (`app/crud/`).

**`app/crud/__init__.py`**

```python
from .crud_user import user
from .crud_organization import organization
from .crud_drone import drone, user_drone_assignment
from .crud_flight_plan import flight_plan
from .crud_waypoint import waypoint # If direct CRUD for waypoints is needed, usually part of flight_plan
from .crud_telemetry_log import telemetry_log
from .crud_restricted_zone import restricted_zone

# The idea is to import crud objects here for easy access, e.g.:
# from app.crud import user, organization
```

**`app/crud/base.py`**

```python
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func # For count

from app.db.base_class import Base
from app.db.utils import get_active_query, apply_soft_delete_filter_to_query_condition

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any, include_deleted: bool = False) -> Optional[ModelType]:
        query = db.query(self.model)
        if not include_deleted and hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        return query.filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> List[ModelType]:
        query = db.query(self.model)
        if not include_deleted and hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        return query.offset(skip).limit(limit).all()
    
    def get_multi_with_filter(
        self, db: Session, *, filter_conditions: Optional[List] = None, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> List[ModelType]:
        query = db.query(self.model)
        if not include_deleted and hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        if filter_conditions:
            for condition in filter_conditions:
                query = query.filter(condition)
        return query.offset(skip).limit(limit).all()

    def get_count(self, db: Session, include_deleted: bool = False) -> int:
        query = db.query(func.count(self.model.id))
        if not include_deleted and hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        return query.scalar_one()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj # Return the deleted object or None

    def soft_remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        if obj and hasattr(self.model, "deleted_at"):
            setattr(obj, "deleted_at", func.now())
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        elif obj: # If no deleted_at, perform hard delete
            return self.remove(db, id=id)
        return None
```

**`app/crud/crud_user.py`**

```python
from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.db.utils import apply_soft_delete_filter_to_query_condition


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str, include_deleted: bool = False) -> Optional[User]:
        query = db.query(User).filter(User.email == email)
        if not include_deleted and hasattr(User, "deleted_at"):
            query = query.filter(User.deleted_at.is_(None))
        return query.first()

    def get_by_iin(self, db: Session, *, iin: str, include_deleted: bool = False) -> Optional[User]:
        query = db.query(User).filter(User.iin == iin)
        if not include_deleted and hasattr(User, "deleted_at"):
            query = query.filter(User.deleted_at.is_(None))
        return query.first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            phone_number=obj_in.phone_number,
            iin=obj_in.iin,
            role=obj_in.role, # Role is now part of UserCreate
            is_active=True, # Default, can be overridden if UserCreate has is_active
            organization_id=getattr(obj_in, 'organization_id', None) # If present in schema
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "new_password" in update_data and update_data["new_password"]:
            hashed_password = get_password_hash(update_data["new_password"])
            del update_data["new_password"] # Don't store plain new_password
            if "current_password" in update_data: # current_password might not be in dict if obj_in is dict
                 del update_data["current_password"]
            db_obj.hashed_password = hashed_password # Set hashed password directly

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not user.is_active: # Do not authenticate inactive users
            return None
        from app.core.security import verify_password # Local import to avoid circularity if security needs User
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_authority_admin(self, user: User) -> bool:
        return user.role == UserRole.AUTHORITY_ADMIN
    
    def is_organization_admin(self, user: User) -> bool:
        return user.role == UserRole.ORGANIZATION_ADMIN

    def get_multi_users(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        role: Optional[UserRole] = None, 
        organization_id: Optional[int] = None,
        include_deleted: bool = False
    ) -> List[User]:
        query = db.query(self.model)
        if not include_deleted:
            query = query.filter(self.model.deleted_at.is_(None))
        
        if role:
            query = query.filter(self.model.role == role)
        if organization_id is not None: # Check for None explicitly for 0
            query = query.filter(self.model.organization_id == organization_id)
            
        return query.order_by(self.model.id).offset(skip).limit(limit).all()

    def set_user_status(self, db: Session, *, user_id: int, is_active: bool) -> Optional[User]:
        db_user = self.get(db, id=user_id)
        if not db_user:
            return None
        db_user.is_active = is_active
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user = CRUDUser(User)
```

**`app/crud/crud_organization.py`**

```python
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.crud.base import CRUDBase
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate # OrganizationCreate might not be used directly

class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):
    def get_by_name(self, db: Session, *, name: str, include_deleted: bool = False) -> Optional[Organization]:
        query = db.query(Organization).filter(Organization.name == name)
        if not include_deleted:
            query = query.filter(Organization.deleted_at.is_(None))
        return query.first()

    def get_by_bin(self, db: Session, *, bin_val: str, include_deleted: bool = False) -> Optional[Organization]:
        query = db.query(Organization).filter(Organization.bin == bin_val)
        if not include_deleted:
            query = query.filter(Organization.deleted_at.is_(None))
        return query.first()

    def get_multi_organizations(
        self, db: Session, *, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> List[Organization]:
        query = db.query(self.model)
        if not include_deleted:
            query = query.filter(self.model.deleted_at.is_(None))
        return query.order_by(self.model.id).offset(skip).limit(limit).all()

    # create method is inherited from CRUDBase.
    # For organization creation with admin, a service layer function is better
    # as it's a transactional operation involving two models.

organization = CRUDOrganization(Organization)
```

**`app/crud/crud_drone.py`**

```python
from typing import Optional, List, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.drone import Drone, DroneStatus
from app.models.user_drone_assignment import UserDroneAssignment
from app.schemas.drone import DroneCreate, DroneUpdate

class CRUDDrone(CRUDBase[Drone, DroneCreate, DroneUpdate]):
    def get_by_serial_number(self, db: Session, *, serial_number: str, include_deleted: bool = False) -> Optional[Drone]:
        query = db.query(Drone).filter(Drone.serial_number == serial_number)
        if not include_deleted:
            query = query.filter(Drone.deleted_at.is_(None))
        return query.first()

    def get_multi_drones_for_user(
        self, 
        db: Session, 
        *, 
        user_id: int, 
        organization_id: Optional[int] = None, # For org admin/pilot
        is_org_admin: bool = False,
        skip: int = 0, 
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[Drone]:
        query = db.query(Drone)
        if not include_deleted:
            query = query.filter(Drone.deleted_at.is_(None))

        if is_org_admin and organization_id is not None:
            # Org admin sees all drones in their organization
            query = query.filter(Drone.organization_id == organization_id)
        elif organization_id is not None: # Org pilot
            # Org pilot sees drones assigned to them in their organization
            query = query.join(UserDroneAssignment, UserDroneAssignment.drone_id == Drone.id)\
                         .filter(UserDroneAssignment.user_id == user_id)\
                         .filter(Drone.organization_id == organization_id) # Ensure drone is in their org
        else: # Solo pilot
            query = query.filter(Drone.solo_owner_user_id == user_id)
        
        return query.order_by(Drone.id).offset(skip).limit(limit).all()

    def get_multi_drones_for_organization(
        self, db: Session, *, organization_id: int, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> List[Drone]:
        query = db.query(Drone).filter(Drone.organization_id == organization_id)
        if not include_deleted:
            query = query.filter(Drone.deleted_at.is_(None))
        return query.order_by(Drone.id).offset(skip).limit(limit).all()

    def get_all_drones_admin(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        organization_id: Optional[int] = None,
        status: Optional[DroneStatus] = None,
        include_deleted: bool = False
    ) -> List[Drone]:
        query = db.query(Drone)
        if not include_deleted:
            query = query.filter(Drone.deleted_at.is_(None))
        
        if organization_id is not None:
            query = query.filter(Drone.organization_id == organization_id)
        if status:
            query = query.filter(Drone.current_status == status)
            
        return query.order_by(Drone.id).offset(skip).limit(limit).all()

drone = CRUDDrone(Drone)


class CRUDUserDroneAssignment(CRUDBase[UserDroneAssignment, Any, Any]): # Schemas not strictly needed for base
    def get_assignment(self, db: Session, *, user_id: int, drone_id: int) -> Optional[UserDroneAssignment]:
        # UserDroneAssignment does not have 'deleted_at' in its strict schema definition
        return db.query(UserDroneAssignment).filter(
            UserDroneAssignment.user_id == user_id,
            UserDroneAssignment.drone_id == drone_id
        ).first()

    def assign_user_to_drone(self, db: Session, *, user_id: int, drone_id: int) -> UserDroneAssignment:
        # Check if already assigned
        existing_assignment = self.get_assignment(db, user_id=user_id, drone_id=drone_id)
        if existing_assignment:
            return existing_assignment # Or raise error if re-assigning is not allowed

        db_obj = UserDroneAssignment(user_id=user_id, drone_id=drone_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def unassign_user_from_drone(self, db: Session, *, user_id: int, drone_id: int) -> Optional[UserDroneAssignment]:
        db_obj = self.get_assignment(db, user_id=user_id, drone_id=drone_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj # Return the deleted object or None

    def get_assignments_for_drone(self, db: Session, *, drone_id: int) -> List[UserDroneAssignment]:
        return db.query(UserDroneAssignment).filter(UserDroneAssignment.drone_id == drone_id).all()

    def get_assignments_for_user(self, db: Session, *, user_id: int) -> List[UserDroneAssignment]:
        return db.query(UserDroneAssignment).filter(UserDroneAssignment.user_id == user_id).all()

user_drone_assignment = CRUDUserDroneAssignment(UserDroneAssignment)
```

**`app/crud/crud_flight_plan.py`**

```python
from typing import Optional, List, Any
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.flight_plan import FlightPlan, FlightPlanStatus
from app.models.waypoint import Waypoint
from app.schemas.flight_plan import FlightPlanCreate, FlightPlanUpdate # FlightPlanUpdate for general updates
from app.schemas.waypoint import WaypointCreate


class CRUDFlightPlan(CRUDBase[FlightPlan, FlightPlanCreate, FlightPlanUpdate]):
    def create_with_waypoints(self, db: Session, *, obj_in: FlightPlanCreate, user_id: int, organization_id: Optional[int] = None, initial_status: FlightPlanStatus) -> FlightPlan:
        db_flight_plan = FlightPlan(
            user_id=user_id,
            drone_id=obj_in.drone_id,
            organization_id=organization_id, # Set if applicable
            planned_departure_time=obj_in.planned_departure_time,
            planned_arrival_time=obj_in.planned_arrival_time,
            notes=obj_in.notes,
            status=initial_status # Set by service layer
        )
        db.add(db_flight_plan)
        # Must flush to get flight_plan.id for waypoints
        db.flush() 
        
        for waypoint_in in obj_in.waypoints:
            db_waypoint = Waypoint(
                flight_plan_id=db_flight_plan.id,
                **waypoint_in.model_dump()
            )
            db.add(db_waypoint)
            
        db.commit()
        db.refresh(db_flight_plan)
        return db_flight_plan

    def get_flight_plan_with_details(self, db: Session, id: int, include_deleted: bool = False) -> Optional[FlightPlan]:
        query = db.query(FlightPlan).options(
            selectinload(FlightPlan.waypoints),
            selectinload(FlightPlan.drone),
            selectinload(FlightPlan.submitter_user)
        ).filter(FlightPlan.id == id)
        
        if not include_deleted:
            query = query.filter(FlightPlan.deleted_at.is_(None))
        return query.first()

    def get_multi_for_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100, status: Optional[FlightPlanStatus] = None, include_deleted: bool = False
    ) -> List[FlightPlan]:
        query = db.query(FlightPlan).filter(FlightPlan.user_id == user_id)
        if not include_deleted:
            query = query.filter(FlightPlan.deleted_at.is_(None))
        if status:
            query = query.filter(FlightPlan.status == status)
        return query.order_by(FlightPlan.planned_departure_time.desc()).offset(skip).limit(limit).all()

    def get_multi_for_organization(
        self, db: Session, *, organization_id: int, skip: int = 0, limit: int = 100, status: Optional[FlightPlanStatus] = None, user_id: Optional[int] = None, include_deleted: bool = False
    ) -> List[FlightPlan]:
        query = db.query(FlightPlan).filter(FlightPlan.organization_id == organization_id)
        if not include_deleted:
            query = query.filter(FlightPlan.deleted_at.is_(None))
        if status:
            query = query.filter(FlightPlan.status == status)
        if user_id:
            query = query.filter(FlightPlan.user_id == user_id)
        return query.order_by(FlightPlan.planned_departure_time.desc()).offset(skip).limit(limit).all()

    def get_all_flight_plans_admin(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        status: Optional[FlightPlanStatus] = None,
        organization_id: Optional[int] = None,
        user_id: Optional[int] = None,
        include_deleted: bool = False
    ) -> List[FlightPlan]:
        query = db.query(FlightPlan)
        if not include_deleted:
            query = query.filter(FlightPlan.deleted_at.is_(None))
        
        if status:
            query = query.filter(FlightPlan.status == status)
        if organization_id is not None:
            query = query.filter(FlightPlan.organization_id == organization_id)
        if user_id is not None:
            query = query.filter(FlightPlan.user_id == user_id)
            
        return query.order_by(FlightPlan.planned_departure_time.desc()).offset(skip).limit(limit).all()

    def update_status(
        self, 
        db: Session, 
        *, 
        db_obj: FlightPlan, 
        new_status: FlightPlanStatus, 
        rejection_reason: Optional[str] = None,
        approver_id: Optional[int] = None, # User ID of approver
        is_org_approval: bool = False # Flag to set correct approver field
    ) -> FlightPlan:
        db_obj.status = new_status
        if rejection_reason:
            db_obj.rejection_reason = rejection_reason
        
        if new_status == FlightPlanStatus.APPROVED:
            db_obj.approved_at = func.now() # Using SQLAlchemy func
            if approver_id:
                if is_org_approval: # This logic might be more complex depending on workflow
                    db_obj.approved_by_organization_admin_id = approver_id
                else: # Authority approval (or solo pilot direct approval)
                    db_obj.approved_by_authority_admin_id = approver_id
        
        # If rejected, clear approval fields
        if new_status in [FlightPlanStatus.REJECTED_BY_ORG, FlightPlanStatus.REJECTED_BY_AUTHORITY]:
            db_obj.approved_at = None
            db_obj.approved_by_organization_admin_id = None
            db_obj.approved_by_authority_admin_id = None

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def start_flight(self, db: Session, *, db_obj: FlightPlan) -> FlightPlan:
        db_obj.status = FlightPlanStatus.ACTIVE
        db_obj.actual_departure_time = func.now()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def complete_flight(self, db: Session, *, db_obj: FlightPlan) -> FlightPlan:
        db_obj.status = FlightPlanStatus.COMPLETED
        db_obj.actual_arrival_time = func.now()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def cancel_flight(self, db: Session, *, db_obj: FlightPlan, cancelled_by_role: str, reason: Optional[str]=None) -> FlightPlan:
        if cancelled_by_role == "PILOT":
            db_obj.status = FlightPlanStatus.CANCELLED_BY_PILOT
        else: # ADMIN (Org or Authority)
            db_obj.status = FlightPlanStatus.CANCELLED_BY_ADMIN
        
        # Add cancellation reason to notes or a new field if desired
        if reason:
            db_obj.notes = f"{db_obj.notes or ''}\nCancellation Reason: {reason}".strip()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_flight_history(self, db: Session, flight_plan_id: int, include_deleted: bool = False) -> Optional[FlightPlan]:
        query = db.query(FlightPlan).options(
            selectinload(FlightPlan.waypoints),
            selectinload(FlightPlan.telemetry_logs).order_by(Waypoint.sequence_order), # Order telemetry if needed by timestamp
            selectinload(FlightPlan.drone),
            selectinload(FlightPlan.submitter_user)
        ).filter(FlightPlan.id == flight_plan_id)

        if not include_deleted:
            query = query.filter(FlightPlan.deleted_at.is_(None))
        return query.first()


flight_plan = CRUDFlightPlan(FlightPlan)

# CRUD for Waypoint (if needed separately, usually managed via FlightPlan)
from app.crud.base import CRUDBase
from app.models.waypoint import Waypoint
from app.schemas.waypoint import WaypointCreate, WaypointUpdate

class CRUDWaypoint(CRUDBase[Waypoint, WaypointCreate, WaypointUpdate]):
    def get_by_flight_plan_id(self, db: Session, *, flight_plan_id: int) -> List[Waypoint]:
        return db.query(Waypoint).filter(Waypoint.flight_plan_id == flight_plan_id).order_by(Waypoint.sequence_order).all()

waypoint = CRUDWaypoint(Waypoint)
```

**`app/crud/crud_telemetry_log.py`**

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.telemetry_log import TelemetryLog
from app.schemas.telemetry import TelemetryLogCreate # TelemetryLogUpdate not typical

class CRUDTelemetryLog(CRUDBase[TelemetryLog, TelemetryLogCreate, Any]): # Update schema is Any
    def create_log(self, db: Session, *, obj_in: TelemetryLogCreate) -> TelemetryLog:
        # Direct creation, no complex logic here usually
        return super().create(db, obj_in=obj_in)

    def get_logs_for_flight(
        self, db: Session, *, flight_plan_id: int, limit: Optional[int] = None
    ) -> List[TelemetryLog]:
        query = db.query(TelemetryLog)\
                  .filter(TelemetryLog.flight_plan_id == flight_plan_id)\
                  .order_by(TelemetryLog.timestamp.asc()) # Asc for chronological order
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_latest_log_for_drone(self, db: Session, *, drone_id: int) -> Optional[TelemetryLog]:
        return db.query(TelemetryLog)\
                 .filter(TelemetryLog.drone_id == drone_id)\
                 .order_by(TelemetryLog.timestamp.desc())\
                 .first()

telemetry_log = CRUDTelemetryLog(TelemetryLog)
```

**`app/crud/crud_restricted_zone.py`**

```python
from typing import Optional, List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.restricted_zone import RestrictedZone
from app.schemas.restricted_zone import RestrictedZoneCreate, RestrictedZoneUpdate

class CRUDRestrictedZone(CRUDBase[RestrictedZone, RestrictedZoneCreate, RestrictedZoneUpdate]):
    def get_by_name(self, db: Session, *, name: str, include_deleted: bool = False) -> Optional[RestrictedZone]:
        query = db.query(RestrictedZone).filter(RestrictedZone.name == name)
        if not include_deleted:
            query = query.filter(RestrictedZone.deleted_at.is_(None))
        return query.first()

    def get_all_active_zones(self, db: Session) -> List[RestrictedZone]:
        # Active means is_active = True AND not soft-deleted
        return db.query(RestrictedZone)\
                 .filter(RestrictedZone.is_active == True, RestrictedZone.deleted_at.is_(None))\
                 .all()

    def get_multi_zones_admin(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100, 
        is_active: Optional[bool] = None,
        include_deleted: bool = False # For admin to see soft-deleted ones
    ) -> List[RestrictedZone]:
        query = db.query(RestrictedZone)
        if not include_deleted: # Default behavior for list is to exclude soft-deleted
             query = query.filter(RestrictedZone.deleted_at.is_(None))
        
        if is_active is not None:
            query = query.filter(RestrictedZone.is_active == is_active)
            
        return query.order_by(RestrictedZone.id).offset(skip).limit(limit).all()

restricted_zone = CRUDRestrictedZone(RestrictedZone)
```

---
Next, `app/api/deps.py` for handling dependencies and authentication.

**`app/api/deps.py`**

```python
from typing import Generator, Optional, List

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.token import TokenPayload
from app.crud import user as crud_user # Renamed to avoid conflict

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token",
    scopes={ # Define scopes based on UserRole for more granular control if needed
        UserRole.AUTHORITY_ADMIN: "Full system access.",
        UserRole.ORGANIZATION_ADMIN: "Manage own organization resources.",
        UserRole.ORGANIZATION_PILOT: "Manage own flights within organization.",
        UserRole.SOLO_PILOT: "Manage own flights and drones.",
    }
)

def get_current_user(
    security_scopes: SecurityScopes, # FastAPI injects this
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("sub") is None:
            raise credentials_exception
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user_id = token_data.sub
    if user_id is None:
        raise credentials_exception
    
    user = crud_user.user.get(db, id=int(user_id)) # crud_user.user to access the instance
    if not user:
        raise credentials_exception
    if not crud_user.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    # Scope checking (optional, can be more granular)
    # For simplicity, we'll check roles directly in role-specific dependencies
    # if security_scopes.scopes:
    #     user_roles_as_scopes = [user.role.value] # User has one role
    #     if not any(s in user_roles_as_scopes for s in security_scopes.scopes):
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Not enough permissions",
    #             headers={"WWW-Authenticate": authenticate_value},
    #         )
    return user

# Role-specific dependencies
def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    # This is a base for authenticated users, already checks active status in get_current_user
    return current_user

def get_current_authority_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.AUTHORITY_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges (Authority Admin required).",
        )
    if not current_user.is_active: # Redundant if get_current_user checks, but good for clarity
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def get_current_organization_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ORGANIZATION_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges (Organization Admin required).",
        )
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    if not current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization Admin not associated with an organization.")
    return current_user

def get_current_organization_member(current_user: User = Depends(get_current_user)) -> User:
    """For either Org Admin or Org Pilot"""
    if current_user.role not in [UserRole.ORGANIZATION_ADMIN, UserRole.ORGANIZATION_PILOT]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user must be an Organization Admin or Organization Pilot.",
        )
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    if not current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not associated with an organization.")
    return current_user

def get_current_pilot(current_user: User = Depends(get_current_user)) -> User:
    """For Solo Pilot or Organization Pilot"""
    if current_user.role not in [UserRole.SOLO_PILOT, UserRole.ORGANIZATION_PILOT]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user must be a Pilot (Solo or Organization).",
        )
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


# Permissions for specific resources
# Example: Check if Org Admin owns the organization for a resource
def verify_organization_access(
    organization_id_in_path: int,
    current_user: User = Depends(get_current_organization_admin) # Ensures user is Org Admin
) -> None:
    if current_user.organization_id != organization_id_in_path:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization's resources."
        )

def verify_user_in_organization(
    user_to_check_id: int, # User ID from path or body
    current_org_admin: User = Depends(get_current_organization_admin),
    db: Session = Depends(get_db)
) -> User:
    user = crud_user.user.get(db, id=user_to_check_id)
    if not user or user.organization_id != current_org_admin.organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, # Or 403
            detail="User not found or does not belong to this organization."
        )
    return user

# Add more specific permission checks as needed
```

---
Next, Service layer for more complex business logic.

**`app/services/__init__.py`**

```python
# This file can be empty or used to import services for easier access
from .flight_service import FlightService
from .nfz_service import NFZService
from .telemetry_service import TelemetryService, ConnectionManager

flight_service = FlightService()
nfz_service = NFZService()
telemetry_service = TelemetryService() # The instance for simulation
connection_manager = ConnectionManager() # The instance for WebSocket connections
```

**`app/services/flight_service.py`**

```python
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.flight_plan import FlightPlan, FlightPlanStatus
from app.models.drone import Drone
from app.schemas.flight_plan import FlightPlanCreate
from app.crud import flight_plan as crud_flight_plan
from app.crud import drone as crud_drone
from app.services.nfz_service import NFZService # For NFZ checks
from app.services.telemetry_service import telemetry_service # To start simulation

class FlightService:
    def __init__(self, nfz_service: NFZService = NFZService()): # Allow injecting for tests
        self.nfz_service = nfz_service

    def submit_flight_plan(
        self, 
        db: Session, 
        *, 
        flight_plan_in: FlightPlanCreate, 
        submitter: User
    ) -> FlightPlan:
        # 1. Validate Drone
        db_drone = crud_drone.drone.get(db, id=flight_plan_in.drone_id)
        if not db_drone:
            raise ValueError("Drone not found.")
        
        # Check drone ownership/assignment based on submitter's role
        if submitter.role == UserRole.SOLO_PILOT:
            if db_drone.solo_owner_user_id != submitter.id:
                raise ValueError("Solo pilot can only submit flights for their own drones.")
            organization_id = None
        elif submitter.role == UserRole.ORGANIZATION_PILOT:
            if not submitter.organization_id or db_drone.organization_id != submitter.organization_id:
                raise ValueError("Organization pilot can only submit flights for drones in their organization.")
            # Check if pilot is assigned to this drone
            assignment = crud_drone.user_drone_assignment.get_assignment(db, user_id=submitter.id, drone_id=db_drone.id)
            if not assignment:
                # Or if org allows any pilot to use any org drone without explicit assignment
                # This rule needs clarification from requirements. Assuming explicit assignment for now.
                raise ValueError("Organization pilot is not assigned to this drone.")
            organization_id = submitter.organization_id
        else:
            raise ValueError("Invalid user role for submitting flight plans.")

        # 2. Perform NFZ Pre-check (Simplified)
        # This would involve checking waypoints against RestrictedZone geometries
        # For now, a placeholder
        nfz_violations = self.nfz_service.check_flight_plan_against_nfzs(db, flight_plan_in.waypoints)
        if nfz_violations:
            # For MVP, we might just raise an error or log it.
            # A real system might allow submission with warnings or require modification.
            raise ValueError(f"Flight plan intersects with No-Fly Zones: {', '.join(nfz_violations)}")

        # 3. Determine initial status
        initial_status: FlightPlanStatus
        if submitter.role == UserRole.SOLO_PILOT:
            initial_status = FlightPlanStatus.PENDING_AUTHORITY_APPROVAL
        elif submitter.role == UserRole.ORGANIZATION_PILOT:
            # Assuming two-step approval for organizations
            initial_status = FlightPlanStatus.PENDING_ORG_APPROVAL 
        else: # Should not happen due to earlier check
            raise ValueError("Cannot determine initial flight plan status for user role.")

        # 4. Create Flight Plan
        created_flight_plan = crud_flight_plan.flight_plan.create_with_waypoints(
            db, 
            obj_in=flight_plan_in, 
            user_id=submitter.id,
            organization_id=organization_id,
            initial_status=initial_status
        )
        return created_flight_plan

    def update_flight_plan_status(
        self,
        db: Session,
        *,
        flight_plan_id: int,
        new_status: FlightPlanStatus,
        actor: User, # User performing the action
        rejection_reason: str | None = None,
    ) -> FlightPlan:
        db_flight_plan = crud_flight_plan.flight_plan.get(db, id=flight_plan_id)
        if not db_flight_plan:
            raise ValueError("Flight plan not found.")

        current_status = db_flight_plan.status
        is_org_approval_step = False

        # State transition logic based on actor's role and current status
        if actor.role == UserRole.ORGANIZATION_ADMIN:
            if db_flight_plan.organization_id != actor.organization_id:
                raise ValueError("Organization Admin cannot modify flight plans outside their organization.")
            
            if current_status == FlightPlanStatus.PENDING_ORG_APPROVAL:
                if new_status == FlightPlanStatus.PENDING_AUTHORITY_APPROVAL: # Org Admin approves, sends to Authority
                    is_org_approval_step = True
                elif new_status == FlightPlanStatus.REJECTED_BY_ORG:
                    if not rejection_reason:
                        raise ValueError("Rejection reason required when rejecting by organization.")
                # Org admin might also directly approve if no authority step is needed (e.g. for certain flights)
                # elif new_status == FlightPlanStatus.APPROVED: # Org Admin self-approves
                #     is_org_approval_step = True 
                else:
                    raise ValueError(f"Invalid status transition from {current_status} to {new_status} by Organization Admin.")
            else:
                raise ValueError(f"Organization Admin cannot change status from {current_status}.")

        elif actor.role == UserRole.AUTHORITY_ADMIN:
            valid_previous_statuses_for_authority = [
                FlightPlanStatus.PENDING_AUTHORITY_APPROVAL,
                FlightPlanStatus.PENDING_ORG_APPROVAL # If solo pilot or orgs submit directly to authority
            ]
            if current_status in valid_previous_statuses_for_authority:
                if new_status == FlightPlanStatus.APPROVED:
                    pass # Authority approves
                elif new_status == FlightPlanStatus.REJECTED_BY_AUTHORITY:
                    if not rejection_reason:
                        raise ValueError("Rejection reason required when rejecting by authority.")
                else:
                    raise ValueError(f"Invalid status transition from {current_status} to {new_status} by Authority Admin.")
            else:
                raise ValueError(f"Authority Admin cannot change status from {current_status}.")
        else:
            raise ValueError("User role not authorized to update flight plan status.")

        return crud_flight_plan.flight_plan.update_status(
            db, 
            db_obj=db_flight_plan, 
            new_status=new_status, 
            rejection_reason=rejection_reason,
            approver_id=actor.id,
            is_org_approval=is_org_approval_step
        )

    def start_flight(self, db: Session, *, flight_plan_id: int, pilot: User) -> FlightPlan:
        db_flight_plan = crud_flight_plan.flight_plan.get(db, id=flight_plan_id)
        if not db_flight_plan:
            raise ValueError("Flight plan not found.")
        if db_flight_plan.user_id != pilot.id:
            raise ValueError("Only the submitting pilot can start the flight.")
        if db_flight_plan.status != FlightPlanStatus.APPROVED:
            raise ValueError(f"Flight plan must be APPROVED to start. Current status: {db_flight_plan.status}")

        started_flight = crud_flight_plan.flight_plan.start_flight(db, db_obj=db_flight_plan)
        
        # Start telemetry simulation for this flight
        telemetry_service.start_flight_simulation(db, flight_plan=started_flight)
        
        return started_flight

    def cancel_flight(
        self, 
        db: Session, 
        *, 
        flight_plan_id: int, 
        actor: User, 
        reason: str | None = None
    ) -> FlightPlan:
        db_flight_plan = crud_flight_plan.flight_plan.get(db, id=flight_plan_id)
        if not db_flight_plan:
            raise ValueError("Flight plan not found.")

        cancelled_by_role_type = "UNKNOWN" # For status CANCELLED_BY_ADMIN or CANCELLED_BY_PILOT

        if actor.role in [UserRole.SOLO_PILOT, UserRole.ORGANIZATION_PILOT]:
            if db_flight_plan.user_id != actor.id:
                raise ValueError("Pilot can only cancel their own flight plans.")
            if db_flight_plan.status not in [FlightPlanStatus.PENDING_ORG_APPROVAL, FlightPlanStatus.PENDING_AUTHORITY_APPROVAL, FlightPlanStatus.APPROVED]:
                raise ValueError(f"Pilot cannot cancel flight in status {db_flight_plan.status}.")
            cancelled_by_role_type = "PILOT"
        
        elif actor.role == UserRole.ORGANIZATION_ADMIN:
            if db_flight_plan.organization_id != actor.organization_id:
                raise ValueError("Organization Admin cannot cancel flights outside their organization.")
            # Org Admin can cancel flights in more states, e.g., PENDING_*, APPROVED, maybe even ACTIVE (emergency)
            # Add specific state checks if needed.
            cancelled_by_role_type = "ADMIN"

        elif actor.role == UserRole.AUTHORITY_ADMIN:
            # Authority Admin can cancel flights in most states
            cancelled_by_role_type = "ADMIN"
        else:
            raise ValueError("User role not authorized to cancel this flight plan.")

        # If flight was active, stop simulation
        if db_flight_plan.status == FlightPlanStatus.ACTIVE:
            telemetry_service.stop_flight_simulation(flight_plan_id)
            # Also update drone status if it was active
            db_drone = crud_drone.drone.get(db, id=db_flight_plan.drone_id)
            if db_drone and db_drone.current_status == DroneStatus.ACTIVE:
                crud_drone.drone.update(db, db_obj=db_drone, obj_in={"current_status": DroneStatus.IDLE})


        return crud_flight_plan.flight_plan.cancel_flight(db, db_obj=db_flight_plan, cancelled_by_role=cancelled_by_role_type, reason=reason)

flight_service = FlightService() # Singleton instance
```

**`app/services/nfz_service.py`**

```python
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.models.restricted_zone import RestrictedZone, NFZGeometryType
from app.schemas.waypoint import WaypointCreate # For checking waypoints
from app.crud import restricted_zone as crud_nfz

# For geometry checks - using a placeholder for now
# from shapely.geometry import Point, Polygon, shape

class NFZService:
    def check_flight_plan_against_nfzs(
        self, db: Session, waypoints: List[WaypointCreate]
    ) -> List[str]: # Returns list of names of violated NFZs
        """
        Checks if any waypoint in the flight plan intersects with active NFZs.
        This is a simplified placeholder. Real implementation needs geometric checks.
        """
        active_nfzs = crud_nfz.restricted_zone.get_all_active_zones(db)
        violated_nfz_names: List[str] = []

        if not active_nfzs:
            return []

        for nfz in active_nfzs:
            for waypoint in waypoints:
                # Placeholder: Simple altitude check
                altitude_ok = True
                if nfz.min_altitude_m is not None and waypoint.altitude_m < nfz.min_altitude_m:
                    altitude_ok = False
                if nfz.max_altitude_m is not None and waypoint.altitude_m > nfz.max_altitude_m:
                    altitude_ok = False
                
                if not altitude_ok:
                    # Basic check: if waypoint altitude is within NFZ vertical bounds
                    # Now check horizontal intersection (highly simplified)
                    # TODO: Implement actual geometric intersection logic here
                    # e.g., using Shapely:
                    # waypoint_geom = Point(waypoint.longitude, waypoint.latitude)
                    # nfz_geom_data = nfz.definition_json
                    # if nfz.geometry_type == NFZGeometryType.CIRCLE:
                    #     center = Point(nfz_geom_data["center_lon"], nfz_geom_data["center_lat"])
                    #     radius_degrees = nfz_geom_data["radius_m"] / 111000 # Rough conversion
                    #     nfz_shape = center.buffer(radius_degrees)
                    # elif nfz.geometry_type == NFZGeometryType.POLYGON:
                    #     nfz_shape = Polygon(nfz_geom_data["coordinates"][0]) # Assuming GeoJSON like structure
                    #
                    # if nfz_shape.intersects(waypoint_geom):
                    #    if nfz.name not in violated_nfz_names:
                    #        violated_nfz_names.append(nfz.name)
                    #    break # Move to next NFZ if one waypoint violates it
                    
                    # Simplified: Assume any NFZ is a potential violation for demo
                    # This is NOT a real check.
                    # For this placeholder, let's say if altitude is within range, it's a potential issue.
                    # This is a very rough approximation and should be replaced.
                    if nfz.name not in violated_nfz_names:
                         # This is just a dummy check for the placeholder
                        if waypoint.latitude > 0 and waypoint.longitude > 0: # Arbitrary condition
                            pass #violated_nfz_names.append(f"{nfz.name} (Placeholder: Altitude conflict at Waypoint {waypoint.sequence_order})")
            # if nfz.name in violated_nfz_names:
            #     continue # Already found violation for this NFZ

        # This function currently returns an empty list.
        # You MUST implement proper geometric checks.
        # Example: if a simple bounding box check fails for any NFZ.
        # For now, we'll return no violations to allow submissions.
        return [] # IMPORTANT: Replace with real logic

    def check_point_against_nfzs(
        self, db: Session, lat: float, lon: float, alt_m: float
    ) -> List[Dict[str, Any]]: # Returns list of violated NFZ details
        """
        Checks a single telemetry point against active NFZs.
        Placeholder for real geometric checks.
        """
        active_nfzs = crud_nfz.restricted_zone.get_all_active_zones(db)
        violations: List[Dict[str, Any]] = []

        if not active_nfzs:
            return []

        # telemetry_point = Point(lon, lat)

        for nfz in active_nfzs:
            # Altitude check
            in_vertical_bounds = True
            if nfz.min_altitude_m is not None and alt_m < nfz.min_altitude_m:
                in_vertical_bounds = False
            if nfz.max_altitude_m is not None and alt_m > nfz.max_altitude_m:
                in_vertical_bounds = False
            
            if not in_vertical_bounds:
                continue # Not within vertical range of this NFZ

            # Horizontal check (TODO: Implement real geometric check)
            # nfz_geom_data = nfz.definition_json
            # if nfz.geometry_type == NFZGeometryType.CIRCLE:
            #     center = Point(nfz_geom_data["center_lon"], nfz_geom_data["center_lat"])
            #     radius_degrees = nfz_geom_data["radius_m"] / 111000 # Rough conversion
            #     nfz_shape = center.buffer(radius_degrees)
            # elif nfz.geometry_type == NFZGeometryType.POLYGON:
            #     nfz_shape = Polygon(nfz_geom_data["coordinates"][0])
            #
            # if nfz_shape.intersects(telemetry_point):
            #     violations.append({"name": nfz.name, "id": nfz.id, "description": "NFZ Breach"})
            
            # Placeholder:
            # if lat > 10 and lon > 10: # Arbitrary condition
            #    violations.append({"name": nfz.name, "id": nfz.id, "description": "NFZ Breach (Placeholder)"})
            pass # No violations for placeholder

        return violations

nfz_service = NFZService()
```

**`app/services/telemetry_service.py`**

```python
import asyncio
import random
import time
from datetime import datetime, timezone
from typing import List, Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.models.flight_plan import FlightPlan, FlightPlanStatus
from app.models.drone import Drone, DroneStatus
from app.models.telemetry_log import TelemetryLog
from app.schemas.telemetry import TelemetryLogCreate, LiveTelemetryMessage
from app.crud import telemetry_log as crud_telemetry_log
from app.crud import drone as crud_drone
from app.crud import flight_plan as crud_flight_plan # For completing flight
from app.db.session import SessionLocal # To create new sessions in async tasks
from app.services.nfz_service import nfz_service # For in-flight NFZ checks


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        # For targeted messages if needed in future (e.g., per organization_id)
        # self.scoped_connections: Dict[Any, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except WebSocketDisconnect:
            self.disconnect(websocket)
        except RuntimeError: # Handle cases where connection might be closing
            self.disconnect(websocket)


    async def broadcast(self, message_data: dict): # Changed to accept dict for JSON
        # message_json = json.dumps(message_data) # Pydantic model will be converted by FastAPI
        disconnected_sockets = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message_data)
            except (WebSocketDisconnect, RuntimeError):
                disconnected_sockets.append(connection)
        
        for ws in disconnected_sockets:
            self.disconnect(ws)


class TelemetryService:
    def __init__(self):
        self.active_simulations: Dict[int, asyncio.Task] = {} # flight_plan_id -> Task
        self.simulation_stop_events: Dict[int, asyncio.Event] = {} # flight_plan_id -> Event

    async def _simulate_flight_telemetry(self, flight_plan_id: int, stop_event: asyncio.Event):
        """Simulates telemetry for a given flight plan."""
        # Create a new DB session for this long-running task
        # This is important because the original request's session will be closed.
        db: Session = SessionLocal()
        try:
            fp = crud_flight_plan.flight_plan.get_flight_plan_with_details(db, id=flight_plan_id)
            if not fp or not fp.waypoints:
                print(f"Flight plan {flight_plan_id} not found or no waypoints for simulation.")
                return

            # Update drone status to ACTIVE
            db_drone = crud_drone.drone.get(db, id=fp.drone_id)
            if db_drone:
                db_drone.current_status = DroneStatus.ACTIVE
                db.add(db_drone)
                db.commit()
                db.refresh(db_drone)

            current_waypoint_index = 0
            num_waypoints = len(fp.waypoints)
            
            # Simplified: Assume linear interpolation between waypoints
            # A real simulation would be much more complex (speed, turns, ascent/descent rates)
            
            # Simulation loop
            while current_waypoint_index < num_waypoints and not stop_event.is_set():
                if current_waypoint_index >= len(fp.waypoints): # Should not happen if loop condition is correct
                    break
                
                target_waypoint = fp.waypoints[current_waypoint_index]
                
                # Simulate movement towards target_waypoint (very basic)
                # For now, let's just "jump" to waypoints every few seconds
                # In a real sim, you'd calculate intermediate points.
                
                lat = target_waypoint.latitude
                lon = target_waypoint.longitude
                alt = target_waypoint.altitude_m
                timestamp = datetime.now(timezone.utc)
                speed_mps = random.uniform(5, 15) # m/s
                heading_degrees = random.uniform(0, 359.9)
                status_message = "ON_SCHEDULE"

                # In-flight NFZ check (using the new DB session)
                nfz_breaches = nfz_service.check_point_against_nfzs(db, lat, lon, alt)
                if nfz_breaches:
                    status_message = f"ALERT_NFZ: Breached {', '.join([b['name'] for b in nfz_breaches])}"
                    # Potentially trigger other alert mechanisms

                # Create and store telemetry log
                log_entry = TelemetryLogCreate(
                    flight_plan_id=fp.id,
                    drone_id=fp.drone_id,
                    timestamp=timestamp,
                    latitude=lat,
                    longitude=lon,
                    altitude_m=alt,
                    speed_mps=speed_mps,
                    heading_degrees=heading_degrees,
                    status_message=status_message,
                )
                db_log_entry = crud_telemetry_log.telemetry_log.create(db, obj_in=log_entry)

                # Update drone's last seen and last telemetry
                if db_drone:
                    db_drone.last_seen_at = timestamp
                    db_drone.last_telemetry_id = db_log_entry.id # type: ignore
                    db.add(db_drone)
                    db.commit() # Commit frequently for updates to be visible

                # Broadcast telemetry via WebSocket
                live_message = LiveTelemetryMessage(
                    flight_id=fp.id,
                    drone_id=fp.drone_id,
                    lat=lat,
                    lon=lon,
                    alt=alt,
                    timestamp=timestamp,
                    speed=speed_mps,
                    heading=heading_degrees,
                    status_message=status_message,
                )
                await connection_manager.broadcast(live_message.model_dump())
                
                # Move to next waypoint after a delay
                await asyncio.sleep(5) # Telemetry update interval
                current_waypoint_index += 1

                if stop_event.is_set():
                    print(f"Simulation for flight {flight_plan_id} stopped by event.")
                    status_message = "FLIGHT_INTERRUPTED" # Or similar
                    # Log one final telemetry point indicating interruption if needed
                    break
            
            # Simulation finished (either completed waypoints or stopped)
            final_status_message = "FLIGHT_COMPLETED"
            if stop_event.is_set() and current_waypoint_index < num_waypoints:
                final_status_message = "FLIGHT_CANCELLED_OR_STOPPED"

            # Update flight plan status to COMPLETED if all waypoints were reached
            # and it wasn't externally stopped (e.g., by cancellation)
            # Re-fetch flight plan to get its current status from DB
            db.refresh(fp) # Refresh fp object
            if not stop_event.is_set() and fp.status == FlightPlanStatus.ACTIVE:
                crud_flight_plan.flight_plan.complete_flight(db, db_obj=fp)
                final_status_message = "FLIGHT_COMPLETED"
            
            # Update drone status to IDLE
            if db_drone:
                db_drone.current_status = DroneStatus.IDLE
                db.add(db_drone)
                db.commit()
            
            print(f"Simulation for flight {flight_plan_id} ended with status: {final_status_message}.")

        except Exception as e:
            print(f"Error during flight simulation for {flight_plan_id}: {e}")
            # Attempt to set drone to UNKNOWN or IDLE on error
            if 'db_drone' in locals() and db_drone:
                db_drone.current_status = DroneStatus.UNKNOWN
                db.add(db_drone)
                db.commit()
        finally:
            db.close() # Ensure the session is closed for this task
            if flight_plan_id in self.active_simulations:
                del self.active_simulations[flight_plan_id]
            if flight_plan_id in self.simulation_stop_events:
                del self.simulation_stop_events[flight_plan_id]


    def start_flight_simulation(self, db: Session, flight_plan: FlightPlan):
        if flight_plan.id in self.active_simulations:
            print(f"Simulation for flight {flight_plan.id} is already active.")
            return

        stop_event = asyncio.Event()
        self.simulation_stop_events[flight_plan.id] = stop_event
        
        # We pass flight_plan.id instead of the whole object
        # because the object might become stale if the DB session that loaded it closes.
        # The async task will create its own DB session.
        task = asyncio.create_task(self._simulate_flight_telemetry(flight_plan.id, stop_event))
        self.active_simulations[flight_plan.id] = task
        print(f"Started simulation for flight {flight_plan.id}")

    def stop_flight_simulation(self, flight_plan_id: int):
        if flight_plan_id in self.simulation_stop_events:
            self.simulation_stop_events[flight_plan_id].set() # Signal the task to stop
            print(f"Stop signal sent for flight simulation {flight_plan_id}")
        else:
            print(f"No active simulation found to stop for flight {flight_plan_id}")
        
        # Task cancellation is an option too, but graceful stop via event is preferred.
        # if flight_plan_id in self.active_simulations:
        #     self.active_simulations[flight_plan_id].cancel()

telemetry_service = TelemetryService() # Singleton instance
connection_manager = ConnectionManager() # Singleton instance
```

---
Next, API Routers (`app/api/routers/`).

I will provide these in the next message as this one is getting very long.
