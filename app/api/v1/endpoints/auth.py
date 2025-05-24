from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Any, Dict, cast
from app.core.security import get_password_hash, create_access_token, verify_password
from app.schemas.auth import (
    UserCreateSolo,
    UserCreateOrganizationPilot,
    OrganizationAdminRegister, 
    Token,
    UserResponse,
    OrganizationWithAdminResponse,
)
from app.schemas.login import LoginRequest
from app.db.database import get_db
from app.models.user import User, UserRole
from app.models.organization import Organization
from datetime import timedelta
from app.core.config import settings
from app.api.deps import get_current_user

router = APIRouter()

def create_user_dict(user_data: Dict) -> Dict:
    """Helper function to create user dictionary for SQLAlchemy model"""
    return {
        "full_name": user_data.get("full_name"),
        "email": user_data.get("email"),
        "hashed_password": user_data.get("hashed_password"),
        "phone_number": user_data.get("phone_number"),
        "iin": user_data.get("iin"),
        "role": user_data.get("role"),
        "organization_id": user_data.get("organization_id"),
        "is_active": True
    }

@router.post("/register/solo-pilot", response_model=UserResponse)
async def register_solo_pilot(*, db: Session = Depends(get_db), user_in: UserCreateSolo) -> Any:
    """Register a new independent pilot."""
    # Check if user exists
    stmt = select(User).where(User.email == user_in.email)
    existing_user = db.execute(stmt).scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create user data dictionary
    user_data = {
        "full_name": user_in.full_name,
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
        "phone_number": user_in.phone_number,
        "iin": user_in.iin,
        "role": UserRole.SOLO_PILOT,
        "organization_id": None,
        "is_active": True
    }

    # Create user
    db_user = User(**create_user_dict(user_data))
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )

    return db_user

@router.post("/register/organization-pilot", response_model=UserResponse)
async def register_organization_pilot(*, db: Session = Depends(get_db), user_in: UserCreateOrganizationPilot) -> Any:
    """Register a new pilot who will be a member of an existing organization."""
    # Check if user exists
    stmt = select(User).where(User.email == user_in.email)
    existing_user = db.execute(stmt).scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Check if organization exists and is active
    stmt = select(Organization).where(
        and_(
            Organization.id == user_in.organization_id,
            Organization.is_active == True
        )
    )
    organization = db.execute(stmt).scalar_one_or_none()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found or is inactive"
        )

    # Create user data dictionary
    user_data = {
        "full_name": user_in.full_name,
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
        "phone_number": user_in.phone_number,
        "iin": user_in.iin,
        "role": UserRole.ORGANIZATION_PILOT,
        "organization_id": user_in.organization_id
    }

    # Create user
    db_user = User(**create_user_dict(user_data))
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )

    return db_user

@router.post("/register/organization-admin", response_model=OrganizationWithAdminResponse)
async def register_organization_admin(*, db: Session = Depends(get_db), org_in: OrganizationAdminRegister) -> Any:
    """Register a new organization with its admin."""
    # Check if organization exists
    stmt = select(Organization).where(Organization.bin == org_in.bin)
    existing_org = db.execute(stmt).scalar_one_or_none()
    
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this BIN already exists"
        )

    # Check if admin email is taken
    stmt = select(User).where(User.email == org_in.admin_email)
    existing_admin = db.execute(stmt).scalar_one_or_none()
    
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create organization
    org_data = {
        "name": org_in.name,
        "bin": org_in.bin,
        "company_address": org_in.company_address,
        "city": org_in.city,
        "is_active": True
    }
    db_org = Organization(**org_data)
    db.add(db_org)
    
    try:
        db.commit()
        db.refresh(db_org)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating organization: {str(e)}"
        )

    # Create admin user
    admin_data = {
        "full_name": org_in.admin_full_name,
        "email": org_in.admin_email,
        "hashed_password": get_password_hash(org_in.admin_password),
        "phone_number": org_in.admin_phone_number,
        "iin": org_in.admin_iin,
        "role": UserRole.ORGANIZATION_ADMIN.value,
        "organization_id": db_org.id,
        "is_active": True
    }
    
    db_admin = User(**create_user_dict(admin_data))
    db.add(db_admin)

    try:
        # Set admin_id in organization
        db_org.admin_id = db_admin.id
        db.commit()
        db.refresh(db_admin)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating admin user: {str(e)}"
        )

    # Convert SQLAlchemy models to Pydantic models
    return {
        "organization": {
            "id": db_org.id,
            "name": db_org.name,
            "bin": db_org.bin,
            "company_address": db_org.company_address,
            "city": db_org.city,
            "is_active": db_org.is_active
        },
        "admin_user": {
            "id": db_admin.id,
            "email": db_admin.email,
            "full_name": db_admin.full_name,
            "phone_number": db_admin.phone_number,
            "iin": db_admin.iin,
            "role": db_admin.role,
            "organization_id": db_admin.organization_id,
            "is_active": db_admin.is_active
        }
    }

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)) -> Any:
    """
    Get access token for user authentication.
    """
    user = db.execute(
        select(User).where(User.email == login_data.email)
    ).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    hashed_pass = cast(str, user.hashed_password)
    if not verify_password(login_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)) -> Any:
    """Get current user information."""
    return current_user
