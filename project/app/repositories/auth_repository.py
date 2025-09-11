from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import User, UserSession


class AuthRepository:
    @staticmethod
    async def create_user(user_data: dict) -> User:
        return await DatabaseModule.post_entity(User, user_data)

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        return await DatabaseModule.get_entity_filtered(User, {"email": email})

    @staticmethod
    async def create_session(
        user_id: int, refresh_token: str, user_agent: str | None = None
    ) -> UserSession:
        return await DatabaseModule.post_entity(
            UserSession,
            {
                "user_id": user_id,
                "refresh_token": refresh_token,
                "user_agent": user_agent,
            },
        )

    @staticmethod
    async def get_session(user_id: int, refresh_token: str) -> UserSession | None:
        return await DatabaseModule.get_entity_filtered(
            UserSession, {"user_id": user_id, "refresh_token": refresh_token}
        )

    @staticmethod
    async def delete_session(user_id: int, refresh_token: str) -> None:
        session = await AuthRepository.get_session(user_id, refresh_token)
        if session:
            await DatabaseModule.remove_entity(UserSession, session.id)
