# backend/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.db.database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.Pilot)
def register_new_pilot(
    *,
    db: Session = Depends(get_db),
    pilot_in: schemas.PilotCreate
):
    """
    Create new pilot.
    """
    pilot = crud.get_pilot_by_email(db, email=pilot_in.email)
    if pilot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A pilot with this email already exists in the system.",
        )
    new_pilot = crud.create_pilot(db=db, pilot=pilot_in)
    return new_pilot

@router.post("/login/access-token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends() # FastAPI's form data dependency
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    'username' field in form_data is used for email.
    """
    pilot = crud.get_pilot_by_email(db, email=form_data.username)
    if not pilot or not security.verify_password(form_data.password, pilot.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not pilot.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive pilot"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": pilot.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# You might add a /logout endpoint later if you implement token blacklisting,
# but for JWT, logout is typically handled client-side by deleting the token.