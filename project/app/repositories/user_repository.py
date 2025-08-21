from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import User


class UserRepository:
    @staticmethod
    async def create_user(user_input: dict) -> User | None:
        return await DatabaseModule.post_entity(User, user_input)

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        return await DatabaseModule.get_entity_filtered(User, {"email": email})
