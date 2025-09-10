"""
Centralized Permission Validation Service

This service handles all permission validations across the application
to ensure users can only access and modify resources they have permission for.
"""

from app.repositories.board_repository import BoardRepository
from app.repositories.column_repository import ColumnRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.workspace_repository import WorkspaceRepository
from app.services.permission_service.permission_service_exception import (
    PermissionServiceException,
    PermissionServiceExceptionInfo,
)
from app.services.user_service.user_service import UserService


class PermissionService:
    """
    Centralized service for handling all permission validations
    """

    @staticmethod
    async def validate_user_workspace_access(
        user_email: str, workspace_id: int
    ) -> None:
        """
        Validates that a user has access to a specific workspace

        Args:
            user_email: Email of the user to validate
            workspace_id: ID of the workspace to validate access to

        Raises:
            PermissionServiceException: If user doesn't have access to workspace
        """
        user = await UserService.get_user_by_email_model(user_email)

        has_access = await WorkspaceRepository.check_user_contain_workspace(
            {"workspace_id": workspace_id, "user_id": user.id}
        )

        if not has_access:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_USER_NOT_IN_WORKSPACE
            )

    @staticmethod
    async def validate_user_board_access(user_email: str, board_id: int) -> None:
        """
        Validates that a user has access to a specific board through:
        1. Workspace membership AND
        2. Board membership OR board ownership

        Args:
            user_email: Email of the user to validate
            board_id: ID of the board to validate access to

        Raises:
            PermissionServiceException: If user doesn't have access to board
        """
        user = await UserService.get_user_by_email_model(user_email)

        # Get board to find its workspace
        board = await BoardRepository.get_board_by_identifier(board_id)
        if not board:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_BOARD_NOT_FOUND
            )

        # First validate user has access to the board's workspace
        await PermissionService.validate_user_workspace_access(
            user_email, board.workspace_id
        )

        # Then validate user is either board owner or board member
        is_board_owner = board.owner_id == user.id
        is_board_member = await BoardRepository.is_board_member(board_id, user.id)

        if not (is_board_owner or is_board_member):
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_USER_NOT_IN_WORKSPACE
            )

    @staticmethod
    async def validate_user_column_access(user_email: str, column_id: int) -> None:
        """
        Validates that a user has access to a specific column
        through board/workspace membership

        Args:
            user_email: Email of the user to validate
            column_id: ID of the column to validate access to

        Raises:
            PermissionServiceException: If user doesn't have access to column
        """
        # Get column to find its board
        column = await ColumnRepository.get_column_by_id(column_id)
        if not column:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_COLUMN_NOT_FOUND
            )

        # Validate user has access to the column's board
        await PermissionService.validate_user_board_access(user_email, column.board_id)

    @staticmethod
    async def validate_user_task_access(user_email: str, task_id: int) -> None:
        """
        Validates that a user has access to a
        specific task through column/board/workspace membership

        Args:
            user_email: Email of the user to validate
            task_id: ID of the task to validate access to

        Raises:
            PermissionServiceException: If user doesn't have access to task
        """
        # Get task to find its column
        task = await TaskRepository.get_task_by_id(task_id)
        if not task:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_TASK_NOT_FOUND
            )

        # Validate user has access to the task's column
        await PermissionService.validate_user_column_access(user_email, task.column_id)

    @staticmethod
    async def validate_board_belongs_to_workspace(
        board_id: int, workspace_id: int
    ) -> None:
        """
        Validates that a board belongs to a specific workspace

        Args:
            board_id: ID of the board to validate
            workspace_id: ID of the workspace to validate against

        Raises:
            PermissionServiceException: If board doesn't belong to workspace
        """
        board = await BoardRepository.get_board_by_identifier(board_id)
        if not board:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_BOARD_NOT_FOUND
            )

        if board.workspace_id != workspace_id:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_BOARD_NOT_IN_WORKSPACE
            )

    @staticmethod
    async def validate_column_belongs_to_board(column_id: int, board_id: int) -> None:
        """
        Validates that a column belongs to a specific board

        Args:
            column_id: ID of the column to validate
            board_id: ID of the board to validate against

        Raises:
            PermissionServiceException: If column doesn't belong to board
        """
        column = await ColumnRepository.get_column_by_id(column_id)
        if not column:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_COLUMN_NOT_FOUND
            )

        if column.board_id != board_id:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_COLUMN_NOT_IN_BOARD
            )

    @staticmethod
    async def validate_task_belongs_to_column(task_id: int, column_id: int) -> None:
        """
        Validates that a task belongs to a specific column

        Args:
            task_id: ID of the task to validate
            column_id: ID of the column to validate against

        Raises:
            PermissionServiceException: If task doesn't belong to column
        """
        task = await TaskRepository.get_task_by_id(task_id)
        if not task:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_TASK_NOT_FOUND
            )

        if task.column_id != column_id:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_TASK_NOT_IN_COLUMN
            )

    @staticmethod
    async def validate_workspace_ownership(user_email: str, workspace_id: int) -> None:
        """
        Validates that a user is the owner of a specific workspace

        Args:
            user_email: Email of the user to validate
            workspace_id: ID of the workspace to validate ownership of

        Raises:
            PermissionServiceException: If user is not the workspace owner
        """
        user = await UserService.get_user_by_email_model(user_email)
        workspace = await WorkspaceRepository.get_workspace_by_id(workspace_id)

        if not workspace:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_WORKSPACE_NOT_FOUND
            )

        if workspace.owner_id != user.id:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_USER_NOT_WORKSPACE_OWNER
            )

    @staticmethod
    async def validate_board_ownership(user_email: str, board_id: int) -> None:
        """
        Validates that a user is the owner of a specific board

        Args:
            user_email: Email of the user to validate
            board_id: ID of the board to validate ownership of

        Raises:
            PermissionServiceException: If user is not the board owner
        """
        user = await UserService.get_user_by_email_model(user_email)
        board = await BoardRepository.get_board_by_identifier(board_id)

        if not board:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_BOARD_NOT_FOUND
            )

        if board.owner_id != user.id:
            raise PermissionServiceException(
                PermissionServiceExceptionInfo.ERROR_USER_NOT_BOARD_OWNER
            )
