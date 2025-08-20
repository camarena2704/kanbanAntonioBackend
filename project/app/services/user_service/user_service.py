from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserInputSchema, UserOutputSchema
from app.services.user_service.user_service_exception import UserServiceExceptionInfo, UserServiceException


class UserService:
    @staticmethod
    async def create_user(user: UserInputSchema) -> UserOutputSchema:
        user_instance = user.model_copy(update={"email": str(user.email).lower()})
        response = await UserRepository.create_user(user_instance.model_dump())

        if not response:
            raise UserServiceException(UserServiceExceptionInfo.ERROR_CREATING_USER)

        return UserOutputSchema(**response.__dict__)
