from typing import Optional, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import TokenData

security = HTTPBearer(auto_error=True)


async def get_current_user(
    db: Session = Depends(get_db),
    auth: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            auth.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = cast(str, payload.get("sub"))
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    stmt = select(User).where(User.email == token_data.email)
    result = db.execute(stmt).scalar_one_or_none()

    if result is None:
        raise credentials_exception

    user = cast(User, result)
    is_active = db.execute(select(User.is_active).where(User.id == user.id)).scalar()

    if not is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


async def get_current_active_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> User:
    is_active = db.execute(
        select(User.is_active).where(User.id == current_user.id)
    ).scalar()
    if not is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def get_current_authority_admin(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> User:
    stmt = select(User.role).where(User.id == current_user.id)
    role = db.execute(stmt).scalar()

    if role != "AUTHORITY_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


async def get_current_organization_admin(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> User:
    stmt = select(User.role).where(User.id == current_user.id)
    role = db.execute(stmt).scalar()

    if role != "ORGANIZATION_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user
