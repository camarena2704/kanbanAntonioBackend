from app.schemas.base_schema import BaseException, BaseExceptionInfo


class PermissionServiceExceptionInfo(BaseExceptionInfo):
    ERROR_USER_NOT_IN_WORKSPACE = (
        4001,
        "User does not have access to this workspace",
        403,
    )
    ERROR_BOARD_NOT_FOUND = (4002, "Board not found", 404)
    ERROR_COLUMN_NOT_FOUND = (4003, "Column not found", 404)
    ERROR_TASK_NOT_FOUND = (4004, "Task not found", 404)
    ERROR_WORKSPACE_NOT_FOUND = (4005, "Workspace not found", 404)
    ERROR_BOARD_NOT_IN_WORKSPACE = (4006, "Board does not belong to workspace", 403)
    ERROR_COLUMN_NOT_IN_BOARD = (4007, "Column does not belong to board", 403)
    ERROR_TASK_NOT_IN_COLUMN = (4008, "Task does not belong to column", 403)
    ERROR_USER_NOT_WORKSPACE_OWNER = (4009, "User is not the workspace owner", 403)
    ERROR_USER_NOT_BOARD_OWNER = (4010, "User is not the board owner", 403)


class PermissionServiceException(BaseException):
    pass
