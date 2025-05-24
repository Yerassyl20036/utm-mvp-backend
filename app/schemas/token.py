# backend/app/schemas/token.py
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    # You can add other claims like user_id, role, etc.
    # sub: Optional[str] = None # 'sub' is standard for subject (often user ID or email)