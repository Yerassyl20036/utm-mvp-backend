from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRole(str, Enum):
    AUTHORITY_ADMIN = "AUTHORITY_ADMIN"
    ORGANIZATION_ADMIN = "ORGANIZATION_ADMIN"
    ORGANIZATION_PILOT = "ORGANIZATION_PILOT"
    SOLO_PILOT = "SOLO_PILOT"


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, description="Full name of the user")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=8, description="Password")
    phone_number: Optional[str] = Field(
        None, description="Phone number (must start with +)"
    )
    iin: Optional[str] = Field(None, description="Kazakhstan ID number (12 digits)")

    @validator("iin")
    def validate_iin(cls, v):
        if v is not None and (not v.isdigit() or len(v) != 12):
            raise ValueError("IIN must be 12 digits")
        return v

    @validator("phone_number")
    def validate_phone(cls, v):
        if v is not None and not v.startswith("+"):
            raise ValueError("Phone number must start with +")
        return v


class UserCreateSolo(UserBase):
    """Schema for solo pilot registration"""

    pass


class UserCreateOrganizationPilot(UserBase):
    """Schema for organization pilot registration"""

    organization_id: int = Field(..., description="ID of the organization to join")


class OrganizationAdminRegister(BaseModel):
    """Schema for organization and its admin registration"""

    # Organization details
    name: str = Field(..., min_length=2, description="Organization name")
    bin: str = Field(..., description="Business Identification Number (12 digits)")
    company_address: str = Field(..., min_length=5, description="Company address")
    city: str = Field(..., min_length=2, description="City name")

    # Admin details
    admin_full_name: str = Field(
        ..., min_length=2, description="Full name of the admin"
    )
    admin_email: EmailStr = Field(..., description="Admin email address")
    admin_password: str = Field(..., min_length=8, description="Admin password")
    admin_phone_number: Optional[str] = Field(
        None, description="Admin phone number (must start with +)"
    )
    admin_iin: Optional[str] = Field(None, description="Admin IIN (12 digits)")

    @validator("bin")
    def validate_bin(cls, v):
        if not v.isdigit() or len(v) != 12:
            raise ValueError("BIN must be 12 digits")
        return v

    @validator("admin_phone_number")
    def validate_phone(cls, v):
        if v is not None and not v.startswith("+"):
            raise ValueError("Phone number must start with +")
        return v

    @validator("admin_iin")
    def validate_iin(cls, v):
        if v is not None and (not v.isdigit() or len(v) != 12):
            raise ValueError("IIN must be 12 digits")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class OrganizationResponse(BaseModel):
    id: int
    name: str
    bin: str
    company_address: str
    city: str
    is_active: bool

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone_number: Optional[str] = None
    iin: Optional[str] = None
    role: str
    organization_id: Optional[int] = None
    is_active: bool

    class Config:
        from_attributes = True


class OrganizationWithAdminResponse(BaseModel):
    organization: OrganizationResponse
    admin_user: UserResponse

    class Config:
        from_attributes = True
