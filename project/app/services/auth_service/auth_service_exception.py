from app.schemas.base_schema import BaseException, BaseExceptionInfo


class AuthServiceExceptionInfo(BaseExceptionInfo):
    ERROR_USER_ALREADY_EXISTS = (6001, "User already exists", 400)
    ERROR_USER_NOT_FOUND = (6002, "User not found", 404)
    ERROR_INVALID_CREDENTIALS = (6003, "Invalid credentials", 401)
    ERROR_SESSION_NOT_FOUND = (6004, "Session not found", 401)
    ERROR_REFRESH_TOKEN_INVALID = (6005, "Refresh token invalid or expired", 401)
    ERROR_PASSWORD_RESET_FAILED = (6006, "Password reset failed", 500)
    ERROR_USER_CREATION_FAILED = (6007, "Failed to create user", 500)


class AuthServiceException(BaseException):
    pass
