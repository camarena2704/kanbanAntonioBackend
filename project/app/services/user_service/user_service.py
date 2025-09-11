from app.core.supabase.supabase_client import get_supabase_admin
from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserOutputSchema, UserUpdateSchema
from app.services.user_service.user_service_exception import (
    UserServiceException,
    UserServiceExceptionInfo,
)


class UserService:
    @staticmethod
    async def get_user_by_email(email: str) -> UserOutputSchema:
        # Fetch user by email from the local database
        user = await UserRepository.get_user_by_email(email)
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)
        # Return user data as a schema instance
        return UserOutputSchema(**user.__dict__)

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserOutputSchema:
        # Fetch user by ID from the local database
        user = await UserRepository.get_user_by_id(user_id)
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)
        # Return user data as a schema instance
        return UserOutputSchema(**user.__dict__)

    @staticmethod
    async def update_user(user_id: int, data: UserUpdateSchema) -> UserOutputSchema:
        # Update user fields in the local database
        user = await UserRepository.update_user(user_id, data.model_dump())
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)
        # Return the updated user as a schema instance
        return UserOutputSchema(**user.__dict__)

    @staticmethod
    async def delete_user(sub: str, email: str) -> UserOutputSchema:
        """
        Deletes a user safely:
        1. Remove all associated sessions
        2. Delete the user from Supabase
        3. Delete the user from the local database
        """
        # Retrieve the user by email from the local database
        user = await UserRepository.get_user_by_email(email)
        if not user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)

        # Delete all user sessions
        sessions = await user.sessions.all()
        for session in sessions:
            await AuthRepository.delete_session(user.id, session.refresh_token)

        # Delete the user in Supabase using their UUID (sub)
        supabase = await get_supabase_admin()
        try:
            await supabase.auth.admin.delete_user(sub)
        except Exception:
            raise UserServiceException(
                UserServiceExceptionInfo.ERROR_DELETING_USER_SUPABASE
            )

        # Delete the user from the local database
        deleted_user = await UserRepository.delete_user(user.id)
        if not deleted_user:
            raise UserServiceException(UserServiceExceptionInfo.USER_NOT_FOUND)

        # Return the deleted user data as a schema instance
        return UserOutputSchema(**deleted_user.__dict__)
