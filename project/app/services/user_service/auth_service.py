import os
from datetime import datetime, timezone, timedelta

from app.repositories.auth_repository import AuthRepository
from app.repositories.token_repository import TokenRepository
from app.schemas.auth_schema import RegisterInputSchema, TokenOutputSchema, TokenInputSchema, LoginInputSchema
from app.services.token_service.token_service import TokenService
from app.services.user_service.auth_service_exception import AuthServiceException, AuthServiceExceptionInfo
from app.utils.auth import create_refresh_token, create_access_token, hash_password, verify_password

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


class AuthService:
    @staticmethod
    async def register(payload: RegisterInputSchema, user_agent: str) -> TokenOutputSchema:
        user_found = await AuthRepository.search_user(str(payload.email))
        if user_found:
            raise AuthServiceException(AuthServiceExceptionInfo.EMAIL_EXISTS)

        payload_dict = payload.model_dump()
        payload_dict["password"] = hash_password(payload_dict["password"])

        user = await AuthRepository.register(payload_dict)
        if not user:
            raise AuthServiceException(AuthServiceExceptionInfo.ERROR_CREATING_USER)

        refresh_token = create_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        await TokenService.create_token(
            TokenInputSchema(user_id=user.id,
                             refresh_token=refresh_token,
                             expires_at=expires_at,
                             user_agent=user_agent)
        )

        access_token = create_access_token({
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
        })

        return TokenOutputSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    async def login(payload: LoginInputSchema, user_agent: str) -> TokenOutputSchema:
        user = await AuthRepository.search_user(str(payload.email))
        if not user or not verify_password(payload.password, user.password):
            raise AuthServiceException(AuthServiceExceptionInfo.INVALID_CREDENTIALS)

        refresh_token = create_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        await TokenService.create_token(TokenInputSchema(
            user_id=user.id,
            refresh_token=refresh_token,
            expires_at=expires_at,
            user_agent=user_agent
        ))

        access_token = create_access_token({
            "sub": str(user.id),
            "username": user.username,
            "email": user.email
        })

        return TokenOutputSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    async def refresh_token(refresh_token: str, user_agent: str) -> TokenOutputSchema:
        token_data = await TokenService.get_token(refresh_token)

        if not token_data or token_data.expires_at < datetime.now(timezone.utc):
            raise AuthServiceException(AuthServiceExceptionInfo.INVALID_REFRESH_TOKEN)

        if token_data.user_agent != user_agent:
            raise AuthServiceException(AuthServiceExceptionInfo.INVALID_REFRESH_TOKEN)

        user = await AuthRepository.get_user_by_id(token_data.user_id)
        if not user:
            raise AuthServiceException(AuthServiceExceptionInfo.USER_NOT_FOUND)

        # Generar nuevos tokens
        new_refresh_token = create_refresh_token()
        new_expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        await TokenRepository.update_token(token_id=token_data.id, data={
            "refresh_token": new_refresh_token,
            "expires_at": new_expires_at,
            "user_agent": user_agent
        })

        new_access_token = create_access_token({
            "sub": str(user.id),
            "username": user.username,
            "email": user.email
        })

        return TokenOutputSchema(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )
