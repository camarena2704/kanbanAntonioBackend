from app.modules.database_module.models.default import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserInputSchema, UserOutputSchema
from app.services.user_service.user_service_exception import (
    UserServiceException,
    UserServiceExceptionInfo,
)


class UserService:
    @staticmethod
    async def create_user(user: UserInputSchema) -> UserOutputSchema:
        user_instance = user.model_copy(update={"email": str(user.email).lower()})
        response = await UserRepository.create_user(user_instance.model_dump())

        if not response:
            raise UserServiceException(UserServiceExceptionInfo.ERROR_CREATING_USER)

        return UserOutputSchema(**response.__dict__)

    @staticmethod
    async def get_user_by_email(email: str) -> User:
        return await UserRepository.get_user_by_email(email)
