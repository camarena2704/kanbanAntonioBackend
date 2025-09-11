from app.schemas.base_schema import BaseException, BaseExceptionInfo


class UserServiceExceptionInfo(BaseExceptionInfo):
    EMAIL_EXISTS = (1001, "Email already exists", 400)
    ERROR_CREATING_USER = (1002, "Error creating user", 500)
    USER_NOT_FOUND = (1005, "User not found", 404)
    ERROR_DELETING_USER_SUPABASE = (1006, "Error deleting user in Supabase", 500)


class UserServiceException(BaseException):
    pass
