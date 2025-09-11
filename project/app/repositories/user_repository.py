from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import User


class UserRepository:
    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        return await DatabaseModule.get_entity_filtered(User, {"email": email})

    @staticmethod
    async def get_user_by_id(user_id: int) -> User | None:
        return await DatabaseModule.get_entity(User, user_id)

    @staticmethod
    async def delete_user(user_id: int) -> User | None:
        return await DatabaseModule.remove_entity(User, user_id)

    @staticmethod
    async def update_user(user_id: int, data: dict) -> User | None:
        return await DatabaseModule.put_entity(User, data, user_id)
