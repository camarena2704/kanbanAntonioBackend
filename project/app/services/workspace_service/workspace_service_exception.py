from app.schemas.base_schema import BaseException, BaseExceptionInfo


class WorkspaceServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_WORKSPACE = (2001, "Error creating workspace", 500)


class WorkspaceServiceException(BaseException):
    pass
