from typing import Any, Dict

from pydantic import BaseModel, EmailStr, field_validator

from app.utils.string_helper import StringHelper


class AuthDataOutputSchema(BaseModel):
    token: str
    payload: Dict[str, Any]


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str

    @field_validator("password")
    def validate_password(v: str) -> str:
        return StringHelper.validate_password_complexity(v)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class ResetPasswordSchema(BaseModel):
    access_token: str
    new_password: str

    @field_validator("new_password", mode="after")
    def validate_password(v: str) -> str:
        return StringHelper.validate_password_complexity(v)


class RefreshSchema(BaseModel):
    refresh_token: str


class LogoutSchema(BaseModel):
    refresh_token: str


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class AuthResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int
    email: EmailStr
