# backend/app/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app import crud, models, schemas
from app.core import security
from app.db.database import get_db
from app.core.config import settings

# This URL should match the path of your token endpoint
# For example, if your login endpoint is at /api/v1/auth/login/access-token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/access-token")

def get_current_pilot(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.Pilot:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = security.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    # You could store user_id in token and fetch by id for slight perf improvement
    # but email is fine for now.
    pilot = crud.get_pilot_by_email(db, email=email)
    if pilot is None:
        raise credentials_exception
    return pilot

def get_current_active_pilot(
    current_pilot: models.Pilot = Depends(get_current_pilot)
) -> models.Pilot:
    if not current_pilot.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive pilot")
    return current_pilot

def get_current_active_admin_pilot(
    current_pilot: models.Pilot = Depends(get_current_active_pilot)
) -> models.Pilot:
    if not current_pilot.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_pilot