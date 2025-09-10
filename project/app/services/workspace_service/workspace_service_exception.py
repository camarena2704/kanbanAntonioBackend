from app.schemas.base_schema import BaseException, BaseExceptionInfo


class WorkspaceServiceExceptionInfo(BaseExceptionInfo):
    ERROR_CREATING_WORKSPACE = (2001, "Error creating workspace", 500)
    ERROR_EXISTING_WORKSPACE = (2002, "Error already existing workspace", 400)
    ERROR_WORKSPACE_NOT_FOUND = (2003, "Workspace not found", 404)
    ERROR_INVITED_USER_NOT_FOUND = (2004, "Invited user not found", 404)
    ERROR_USER_ALREADY_IN_WORKSPACE = (
        2005,
        "User is already a member of this workspace",
        400,
    )
    ERROR_USER_TO_REMOVE_NOT_FOUND = (2006, "User to remove not found", 404)
    ERROR_USER_NOT_IN_WORKSPACE = (2007, "User is not a member of this workspace", 400)
    ERROR_CANNOT_REMOVE_WORKSPACE_OWNER = (2008, "Cannot remove workspace owner", 403)


class WorkspaceServiceException(BaseException):
    pass
