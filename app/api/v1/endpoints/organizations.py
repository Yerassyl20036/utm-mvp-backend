from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Any

from app.db.database import get_db
from app.models.organization import Organization
from app.schemas.auth import OrganizationResponse # Assuming OrganizationResponse is in auth.py
from app.api.deps import get_current_user # For authentication/authorization if needed
from app.models.user import User # For type hinting current_user

router = APIRouter()

@router.get("/", response_model=List[OrganizationResponse])
async def read_organizations(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: User = Depends(get_current_user) # Uncomment if endpoint needs authentication
) -> Any:
    """
    Retrieve all organizations.
    
    This endpoint allows for retrieving a list of all organizations,
    with support for pagination (skip, limit).
    
    # Optional: Add authorization checks here if needed, e.g.
    # if not current_user.role == "AUTHORITY_ADMIN":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    """
    stmt = select(Organization).offset(skip).limit(limit).where(Organization.is_active == True)
    organizations = db.execute(stmt).scalars().all()
    return organizations