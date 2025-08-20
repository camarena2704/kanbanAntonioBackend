from app.schemas.base_schema import BaseException, BaseExceptionInfo


class AuthServiceExceptionInfo(BaseExceptionInfo):
    EMAIL_EXISTS = (1001, "Email already exists", 400)
    ERROR_CREATING_USER = (1002, "Error creating user", 500)
    INVALID_CREDENTIALS = (1003, "Invalid credentials", 401)
    INVALID_REFRESH_TOKEN = (1004, "Invalid refresh token", 401)
    USER_NOT_FOUND = (1005, "User not found", 404)


class AuthServiceException(BaseException):
    pass
