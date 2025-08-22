from app.schemas.base_schema import BaseException, BaseExceptionInfo


class WorkspaceServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_WORKSPACE = (2001, "Error creating workspace", 500)
    ERROR_EXISTING_WORKSPACE = (2002, "Error already existing workspace", 400)


class WorkspaceServiceException(BaseException):
    pass
