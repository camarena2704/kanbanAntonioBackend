from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import User


class AuthRepository:
    @staticmethod
    async def register(payload: dict) -> User | None:
       return await DatabaseModule.post_entity(User, payload)

    @staticmethod
    async def search_user(email: str) -> User | None:
        return await DatabaseModule.get_entity_filtered(User, {"email": email})
    @staticmethod
    async def get_user_by_id(user_id: int) -> User | None:
        return await DatabaseModule.get_entity_filtered(User, {"id": user_id})