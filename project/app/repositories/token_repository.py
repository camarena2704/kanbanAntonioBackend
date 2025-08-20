from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Token


class TokenRepository:
    @staticmethod
    async def create_token(payload: dict) -> Token | None:
        return await DatabaseModule.post_entity(Token, payload)

    @staticmethod
    async def delete_existing(user_id: int, user_agent: str):
        token = await Token.filter(user_id=user_id, user_agent=user_agent).first()
        if token:
            await token.delete()

    @staticmethod
    async def get_token_by_refresh_token(refresh_token: str) -> Token | None:
        return await Token.filter(refresh_token=refresh_token).first()

    @staticmethod
    async def delete_token(token_id: int):
        await Token.filter(id=token_id).delete()

    @staticmethod
    async def update_token(token_id: int, data: dict) -> Token | None:
        await Token.filter(id=token_id).update(**data)
        return await Token.filter(id=token_id).first()