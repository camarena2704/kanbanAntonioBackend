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
    """
    Register a new user in the system.

    Creates a new user account with the provided registration data
    and generates authentication tokens.
    The user agent is captured for session tracking purposes.

    Parameters:
    - data: User registration information including email, password, and profile details
    - request: FastAPI request object to extract user agent information

    Returns:
    - AuthResponseSchema: Contains access token, refresh token, and user information
    """
    user_agent = request.headers.get("user-agent")
    return await AuthService.register(data, user_agent)


@router.post("/login", response_model=AuthResponseSchema)
async def login(data: LoginSchema, request: Request):
    """
    Authenticate a user and create a new session.

    Validates user credentials and generates new authentication tokens.
    The user agent is captured for session tracking and security purposes.

    Parameters:
    - data: User login credentials (email and password)
    - request: FastAPI request object to extract user agent information

    Returns:
    - AuthResponseSchema: Contains access token, refresh token, and user information
    """
    user_agent = request.headers.get("user-agent")
    return await AuthService.login(data, user_agent)


@router.post("/refresh", response_model=AuthResponseSchema)
async def refresh(data: RefreshSchema, token_data=Depends(decode_token)):
    """
    Refresh the access token using a valid refresh token.

    Generates a new access token when provided with a valid refresh token.
    This endpoint requires authentication with the current access token.

    Parameters:
    - data: Contains the refresh token to use for generating a new access token
    - token_data: Current access token data extracted from the authorization header

    Returns:
    - AuthResponseSchema: Contains new access token, refresh token, and user information
    """
    user_email = token_data.payload.get("email")
    user = await UserService.get_user_by_email(user_email)
    return await AuthService.refresh(data, user.id)


@router.post("/logout")
async def logout(data: LogoutSchema, token_data=Depends(decode_token)):
    """
    Log out a user and invalidate their current session.

    Terminates the user's active session and invalidates their refresh token.
    This endpoint requires authentication with the current access token.

    Parameters:
    - data: Contains the refresh token to invalidate
    - token_data: Current access token data extracted from the authorization header

    Returns:
    - Success message or status indicating the logout was successful
    """
    user_email = token_data.payload.get("email")
    user = await UserService.get_user_by_email(user_email)
    return await AuthService.logout(data, user.id)


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordSchema):
    """
    Initiate the password reset process for a user.

    Sends a password reset email to the user's registered email address.
    The email contains a link with a time-limited token for resetting the password.

    Parameters:
    - data: Contains the email address of the user requesting password reset

    Returns:
    - Success message indicating that the password reset email was sent
    """
    return await AuthService.forgot_password(data)


@router.post("/reset-password")
async def reset_password(data: ResetPasswordSchema):
    """
    Reset a user's password using the token received via email.

    Validates the reset token and updates the user's password in the system.
    This endpoint does not require authentication as it's used in the
    password recovery flow.

    Parameters:
    - data: Contains the reset token and the new password

    Returns:
    - Success message indicating that the password was successfully reset
    """
    return await AuthService.reset_password(data)
