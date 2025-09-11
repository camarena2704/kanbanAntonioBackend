from fastapi import APIRouter, Depends, Request

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import (
    AuthResponseSchema,
    ForgotPasswordSchema,
    LoginSchema,
    LogoutSchema,
    RefreshSchema,
    RegisterSchema,
    ResetPasswordSchema,
)
from app.services.auth_service.auth_service import AuthService
from app.services.user_service.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=AuthResponseSchema)
async def register(data: RegisterSchema, request: Request):
    user_agent = request.headers.get("user-agent")
    return await AuthService.register(data, user_agent)


@router.post("/login", response_model=AuthResponseSchema)
async def login(data: LoginSchema, request: Request):
    """Login user and create session"""
    user_agent = request.headers.get("user-agent")
    return await AuthService.login(data, user_agent)


@router.post("/refresh", response_model=AuthResponseSchema)
async def refresh(data: RefreshSchema, token_data=Depends(decode_token)):
    """Refresh access token using refresh token"""
    user_email = token_data.payload.get("email")
    user = await UserService.get_user_by_email(user_email)
    return await AuthService.refresh(data, user.id)


@router.post("/logout")
async def logout(data: LogoutSchema, token_data=Depends(decode_token)):
    """Logout and remove session"""
    user_email = token_data.payload.get("email")
    user = await UserService.get_user_by_email(user_email)
    return await AuthService.logout(data, user.id)


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordSchema):
    """Send password reset email"""
    return await AuthService.forgot_password(data)


@router.post("/reset-password")
async def reset_password(data: ResetPasswordSchema):
    """Reset password using access token from email"""
    return await AuthService.reset_password(data)
