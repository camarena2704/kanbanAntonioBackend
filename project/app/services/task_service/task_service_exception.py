from app.schemas.base_schema import BaseException, BaseExceptionInfo


class TaskServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_TASK = (5001, "Error creating task", 500)
    ERROR_EXISTING_TASK_IN_BOARD = (5002, "Error already existing task in this board", 400)


class TaskServiceException(BaseException):
    pass
