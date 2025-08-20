from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel, EmailStr


class RegisterInputSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginInputSchema(BaseModel):
    email: EmailStr
    password: str


class TokenOutputSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenInputSchema(BaseModel):
    user_id: int
    refresh_token: str
    expires_at: datetime
    user_agent: str


class RefreshTokenInputSchema(BaseModel):
    refresh_token: str

class AuthDataOutputSchema(BaseModel):
    token: str
    payload: Dict[str, Any]