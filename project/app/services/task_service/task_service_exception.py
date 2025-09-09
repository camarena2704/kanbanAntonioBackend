from app.schemas.base_schema import BaseException, BaseExceptionInfo


class TaskServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_TASK = (5001, "Error creating task", 500)
    ERROR_EXISTING_TASK_IN_BOARD = (
        5002,
        "Error already existing task in this board",
        400,
    )
    ERROR_TASK_NOT_FOUND = (5003, "Error creating task", 404)
    ERROR_UPDATING_TASK = (5004, "Error updating task", 500)


class TaskServiceException(BaseException):
    pass
