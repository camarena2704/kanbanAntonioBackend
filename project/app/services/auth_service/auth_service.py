from supabase_auth.errors import AuthApiError, AuthRetryableError

from app.core.supabase.supabase_client import get_supabase
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import (
    AuthResponseSchema,
    ForgotPasswordSchema,
    LoginSchema,
    LogoutSchema,
    RefreshSchema,
    RegisterSchema,
    ResetPasswordSchema,
)
from app.services.auth_service.auth_service_exception import (
    AuthServiceException,
    AuthServiceExceptionInfo,
)
from app.utils.timer_helper import utc_now


class AuthService:
    @staticmethod
    async def register(
        data: RegisterSchema, user_agent: str = None
    ) -> AuthResponseSchema:
        """
        Secure user registration process:
        1. Register user in Supabase.
        2. Register user in local database.
        3. Create session if refresh_token is returned by Supabase.
        4. Rollback Supabase registration if local database insertion fails.
        Does not reveal whether the email already exists.
        """
        supabase = await get_supabase()
        try:
            response = await supabase.auth.sign_up(
                {"email": data.email, "password": data.password}
            )
        except (AuthApiError, AuthRetryableError) as e:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_USER_CREATION_FAILED
            ) from e

        if not response.user:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_USER_CREATION_FAILED
            )

        try:
            user = await AuthRepository.create_user(
                {"email": data.email, "name": data.name, "surname": data.surname}
            )
        except Exception as e:
            # Rollback Supabase registration if local DB insertion fails
            try:
                await supabase.auth.admin.delete_user(user_id=response.user.id)
            except (AuthApiError, AuthRetryableError):
                pass
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_USER_CREATION_FAILED
            ) from e

        if response.session:
            await AuthRepository.create_session(
                user_id=user.id,
                refresh_token=response.session.refresh_token,
                user_agent=user_agent,
            )

        return AuthResponseSchema(
            access_token=response.session.access_token if response.session else "",
            refresh_token=response.session.refresh_token if response.session else "",
            user_id=user.id,
            email=user.email,
        )

    @staticmethod
    async def login(data: LoginSchema, user_agent: str = None) -> AuthResponseSchema:
        """
        Authenticate user using Supabase.
        Returns a generic invalid credentials error if authentication fails.
        """
        user = await AuthRepository.get_user_by_email(str(data.email))
        if not user:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_INVALID_CREDENTIALS
            )
        supabase = await get_supabase()
        try:
            response = await supabase.auth.sign_in_with_password(
                {"email": data.email, "password": data.password}
            )
        except (AuthApiError, AuthRetryableError) as e:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_INVALID_CREDENTIALS
            ) from e

        await AuthRepository.create_session(
            user_id=user.id,
            refresh_token=response.session.refresh_token,
            user_agent=user_agent,
        )
        return AuthResponseSchema(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=user.id,
            email=user.email,
        )

    @staticmethod
    async def refresh(data: RefreshSchema, user_id: int) -> AuthResponseSchema:
        """
        Refresh user access token using a valid refresh token.
        Updates the last_used_at timestamp in the local session.
        """
        # Get session from DB
        session = await AuthRepository.get_session(user_id, data.refresh_token)
        if not session:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_REFRESH_TOKEN_INVALID
            )

        # Ask Supabase to refresh the session
        supabase = await get_supabase()
        try:
            response = await supabase.auth.refresh_session(data.refresh_token)
        except (AuthApiError, AuthRetryableError) as e:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_REFRESH_TOKEN_INVALID
            ) from e
        except Exception as e:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_REFRESH_TOKEN_INVALID
            ) from e

        # Update last used timestamp in local DB
        session.last_used_at = utc_now()
        await session.save()

        # Load user from session relationship
        user = await session.user

        return AuthResponseSchema(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=user.id,
            email=user.email,
        )

    @staticmethod
    async def logout(data: LogoutSchema, user_id: int):
        """
        Delete the session associated with the given refresh token.
        """
        await AuthRepository.delete_session(user_id, data.refresh_token)
        return {"message": "Logged out successfully"}

    @staticmethod
    async def forgot_password(data: ForgotPasswordSchema):
        """
        Sends a password reset email using Supabase.
        """
        supabase = await get_supabase()
        try:
            await supabase.auth.reset_password_email(data.email)
        except (AuthApiError, AuthRetryableError) as e:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_PASSWORD_RESET_FAILED
            ) from e
        except Exception as e:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_PASSWORD_RESET_FAILED
            ) from e
        return {"message": "Password reset email sent successfully"}

    @staticmethod
    async def reset_password(data: ResetPasswordSchema):
        """
        Updates the user's password using the provided access token.
        """
        supabase = await get_supabase()
        try:
            await supabase.auth.update_user(
                {"password": data.new_password}, data.access_token
            )
        except (AuthApiError, AuthRetryableError) as e:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_PASSWORD_RESET_FAILED
            ) from e
        except Exception as e:
            raise AuthServiceException(
                AuthServiceExceptionInfo.ERROR_PASSWORD_RESET_FAILED
            ) from e
        return {"message": "Password updated successfully"}
