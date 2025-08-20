from app.schemas.base_schema import BaseException, BaseExceptionInfo


class ExampleServiceExceptionInfo(BaseExceptionInfo):
    CANDIDACY_NOT_FOUND = (1001, "Example not found", 404)


class ExampleServiceException(BaseException):
    pass
