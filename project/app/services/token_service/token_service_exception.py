from app.schemas.base_schema import BaseException, BaseExceptionInfo


class TokenServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_TOKEN = (2001, "Error creating token", 500)


class TokenServiceException(BaseException):
    pass
