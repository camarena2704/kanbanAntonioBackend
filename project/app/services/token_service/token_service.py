import os
from datetime import datetime, timedelta, timezone
from app.modules.database_module.models.default import Token
from app.repositories.token_repository import TokenRepository
from app.schemas.auth_schema import TokenInputSchema, RefreshTokenInputSchema
from app.utils.auth import create_access_token, create_refresh_token

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


class TokenService:
    @staticmethod
    async def create_token(payload: TokenInputSchema) -> Token:
        await TokenRepository.delete_existing(payload.user_id, payload.user_agent)
        return await TokenRepository.create_token(payload.model_dump())

    @staticmethod
    async def refresh_token(data: RefreshTokenInputSchema):
        token_db = await TokenRepository.get_token_by_refresh_token(data.refresh_token)
        if not token_db:
            return None

        if token_db.expires_at < datetime.now(timezone.utc):
            await TokenRepository.delete_token(token_db.id)
            return None

        new_access_token = create_access_token({"sub": str(token_db.user_id)})
        new_refresh_token = create_refresh_token()

        await TokenRepository.update_token(
            token_id=token_db.id,
            data={
                "refresh_token": new_refresh_token,
                "expires_at": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
                "user_agent": data.user_agent,
            }
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    async def get_token(refresh_token: str) -> Token | None:
        return await TokenRepository.get_token_by_refresh_token(refresh_token)
