from app.schemas.base_schema import BaseException, BaseExceptionInfo


class BoardServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_BOARD = (3001, "Error creating board", 500)
    ERROR_UPDATING_BOARD = (3002, "Error updating board", 500)
    ERROR_EXISTING_BOARD_IN_WORKSPACE = (
        3003,
        "Error already existing board in this workspace",
        400,
    )
    ERROR_USER_NOT_CONTAIN_WORKSPACE = (
        3004,
        "User does not belong to this workspace",
        400,
    )
    ERROR_BOARD_NOT_FOUND = (3005, "Board not found", 404)
    ERROR_INVITED_USER_NOT_FOUND = (3006, "Invited user not found", 404)
    ERROR_USER_ALREADY_IN_BOARD = (3007, "User is already a member of this board", 400)
    ERROR_USER_TO_REMOVE_NOT_FOUND = (3008, "User to remove not found", 404)
    ERROR_CANNOT_REMOVE_BOARD_OWNER = (3009, "Cannot remove board owner", 403)
    ERROR_USER_NOT_IN_BOARD = (3010, "User is not a member of this board", 400)


class BoardServiceException(BaseException):
    pass
