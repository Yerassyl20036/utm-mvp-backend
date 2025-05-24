# backend/app/schemas/auth.py
# (If you prefer, you can put LoginRequest in pilot.py or token.py)
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    username: EmailStr # FastAPI's OAuth2PasswordRequestForm expects 'username'
    password: str