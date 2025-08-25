from app.schemas.base_schema import BaseException, BaseExceptionInfo


class BoardServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_BOARD = (3001, "Error creating board", 500)
    ERROR_EXISTING_BOARD_IN_WORKSPACE = (3002, "Error already existing board in this workspace", 400)
    ERROR_USER_NOT_CONTAIN_WORKSPACE = (3003, "User does not belong to this workspace", 400)



class BoardServiceException(BaseException):
    pass
