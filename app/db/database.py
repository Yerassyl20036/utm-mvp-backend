from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base_class import Base # Import your Base

# For synchronous operations (FastAPI default)
engine = create_engine(
    settings.ASSEMBLED_DATABASE_URL,
    pool_pre_ping=True,
    # connect_args={"options": "-c timezone=utc"} # Optional: ensure timezone consistency
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This function can be used to create tables (e.g., for tests or initial setup if not using Alembic for everything)
# But Alembic will be our primary tool for schema management.
def init_db():
    # Import all modules here that define models so that
    # Base has them registered before calling create_all()
    # This is crucial or Base.metadata will be empty.
    # We will populate app.models.__init__ later to import all models.
    # For now, this is a placeholder.
    # from app import models # This will import __init__.py from models folder
    
    print("Initializing database and creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")