from app.schemas.base_schema import BaseException, BaseExceptionInfo


class ColumnServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_COLUMN = (4001, "Error creating column", 500)
    ERROR_EXISTING_COLUMN_IN_BOARD = (4002, "Column already exists in this board", 400)
    ERROR_USER_NOT_CONTAIN_BOARD = (4003, "User does not belong to this board", 400)
    ERROR_COLUMN_NOT_FOUND = (4004, "Column not found", 404)
    ERROR_UPDATING_COLUMN = (4005, "Error updating column", 500)


class ColumnServiceException(BaseException):
    pass
