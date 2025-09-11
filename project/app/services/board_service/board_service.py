from tortoise.expressions import Q

from app.repositories.board_repository import BoardRepository
from app.schemas.board_schema import (
    BoardCreateSchema,
    BoardFavoriteSchema,
    BoardFilterByNameSchema,
    BoardInvitationSchema,
    BoardMemberOutputSchema,
    BoardOutputSchema,
    BoardPaginateSchema,
    BoardRemoveMemberSchema,
)
from app.schemas.workspace_schema import WorkspaceFilterByUserInputSchema
from app.services.board_service.board_service_exception import (
    BoardServiceException,
    BoardServiceExceptionInfo,
)
from app.services.permission_service.permission_service import PermissionService
from app.services.user_service.user_service import UserService
from app.services.workspace_service.workspace_service import WorkspaceService


class BoardService:
    @staticmethod
    async def create_board(
        board: BoardCreateSchema, user_email: str
    ) -> BoardOutputSchema:
        # Get user by email
        user = await UserService.get_user_by_email_model(user_email)

        # Validate that the user belongs to the workspace
        is_user_contain_workspace = await WorkspaceService.check_user_contain_workspace(
            WorkspaceFilterByUserInputSchema(
                workspace_id=board.workspace_id, user_id=user.id
            )
        )
        if not is_user_contain_workspace:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_NOT_CONTAIN_WORKSPACE
            )

        # Validate that the board name does not exist in the workspace
        is_name_board_exist = await BoardService.get_board_by_name_and_workspace_id(
            BoardFilterByNameSchema(name=board.name, workspace_id=board.workspace_id)
        )
        if is_name_board_exist:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_EXISTING_BOARD_IN_WORKSPACE
            )

        # Create the board with owner_id from authenticated user
        payload = {
            "name": board.name.strip(),
            "workspace_id": board.workspace_id,
            "owner_id": user.id,
        }
        board_model = await BoardRepository.create_board(payload)
        if not board_model:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_CREATING_BOARD)

        response = BoardOutputSchema(**board_model.__dict__)

        # Auto-add creator as board member
        await board_model.members.add(user)

        # Add to favorites if indicated using repository methods
        if board.is_favorite:
            await BoardRepository.add_user_to_favorites(board_model, user)
            response.is_favorite = True

        return response

    @staticmethod
    async def get_board_by_name_and_workspace_id(
        board_filtered: BoardFilterByNameSchema,
    ) -> BoardOutputSchema | None:
        # Retrieve a board by name within a workspace
        board = await BoardRepository.get_board_by_name_and_workspace(
            BoardFilterByNameSchema(
                name=board_filtered.name.strip(),
                workspace_id=board_filtered.workspace_id,
            ).model_dump()
        )
        return BoardOutputSchema(**board.__dict__) if board else None

    @staticmethod
    async def get_all_board_paginate_by_workspace_id(
        user_email: str,
        workspace_id: int,
        is_favorite: bool,
        page: int = 0,
        limit: int = 25,
    ) -> BoardPaginateSchema:
        # Get user by email
        user = await UserService.get_user_by_email_model(user_email)

        # Validate workspace
        is_user_contain_workspace = await WorkspaceService.check_user_contain_workspace(
            WorkspaceFilterByUserInputSchema(workspace_id=workspace_id, user_id=user.id)
        )
        if not is_user_contain_workspace:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_NOT_CONTAIN_WORKSPACE
            )

        # Handle favorite vs non-favorite boards differently
        if is_favorite:
            # Get boards that are favorites for this user
            query = Q(workspace_id=workspace_id) & Q(users__id=user.id)
            response = (
                await BoardRepository.get_all_board_filter_paginate_by_workspace_id(
                    {},
                    page,
                    limit,
                    query=query,
                )
            )
        else:
            # Get non-favorite boards using the specialized method
            response = await BoardRepository.get_non_favorite_boards_paginated(
                workspace_id=workspace_id, user_id=user.id, page=page, limit=limit
            )

        if not response:
            return BoardPaginateSchema(total=0, data=[])

        boards = [
            BoardOutputSchema(**board.__dict__, is_favorite=is_favorite)
            for board in response[0]
        ]
        return BoardPaginateSchema(data=boards, total=response[1])

    @staticmethod
    async def get_board_by_identifier(board_id: int) -> BoardOutputSchema:
        # Retrieve a board by its identifier
        board = await BoardRepository.get_board_by_identifier(board_id)
        if not board:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_BOARD_NOT_FOUND)
        return BoardOutputSchema(**board.__dict__)

    @staticmethod
    async def update_favorite_board(
        board_id: int, user_email: str
    ) -> BoardOutputSchema:
        # Get user by email
        user = await UserService.get_user_by_email_model(user_email)

        # Retrieve the board
        board = await BoardRepository.get_board_by_identifier(board_id)
        if not board:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_BOARD_NOT_FOUND)

        # Validate that the user belongs to the workspace
        is_user_contain_workspace = await WorkspaceService.check_user_contain_workspace(
            WorkspaceFilterByUserInputSchema(
                workspace_id=board.workspace_id, user_id=user.id
            )
        )
        if not is_user_contain_workspace:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_NOT_CONTAIN_WORKSPACE
            )

        # Check if the board is already a favorite for this user
        is_favorite = await BoardRepository.is_favorite_board(board_id, user.id)

        # Update favorite status using the repository
        response = BoardOutputSchema(**board.__dict__)
        if is_favorite:
            await BoardRepository.remove_user_from_favorites(board, user)
            response.is_favorite = False
        else:
            await BoardRepository.add_user_to_favorites(board, user)
            response.is_favorite = True

        return response

    @staticmethod
    async def is_favorite_board(favorite_schema: BoardFavoriteSchema) -> bool:
        # Check if a board is marked as favorite by a user
        return await BoardRepository.is_favorite_board(
            favorite_schema.board_id, favorite_schema.user_id
        )

    @staticmethod
    async def invite_user_to_board(
        invitation: BoardInvitationSchema, inviter_email: str
    ) -> BoardInvitationSchema:
        """Invite a user to a board (only board owner can do this)"""
        # Validate inviter is board owner
        await PermissionService.validate_board_ownership(
            inviter_email, invitation.board_id
        )

        # Get the user being invited
        try:
            invited_user = await UserService.get_user_by_email_model(
                invitation.invited_user_email
            )
        except Exception:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_INVITED_USER_NOT_FOUND
            )

        # Get board
        board = await BoardRepository.get_board_by_identifier(invitation.board_id)

        # Check if user is already a member
        is_already_member = await BoardRepository.is_board_member(
            invitation.board_id, invited_user.id
        )

        if is_already_member:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_ALREADY_IN_BOARD
            )

        # Add user to board members
        await board.members.add(invited_user)

        return invitation

    @staticmethod
    async def remove_user_from_board(
        removal: BoardRemoveMemberSchema, remover_email: str
    ) -> BoardRemoveMemberSchema:
        """Remove a user from a board (only board owner can do this)"""
        # Validate remover is board owner
        await PermissionService.validate_board_ownership(
            remover_email, removal.board_id
        )

        # Get the user being removed
        try:
            user_to_remove = await UserService.get_user_by_email_model(
                removal.user_email_to_remove
            )
        except Exception:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_TO_REMOVE_NOT_FOUND
            )

        # Get board
        board = await BoardRepository.get_board_by_identifier(removal.board_id)

        # Prevent removing the board owner
        if board.owner_id == user_to_remove.id:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_CANNOT_REMOVE_BOARD_OWNER
            )

        # Check if user is a member
        is_member = await BoardRepository.is_board_member(
            removal.board_id, user_to_remove.id
        )

        if not is_member:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_NOT_IN_BOARD
            )

        # Remove user from board
        await board.members.remove(user_to_remove)

        return removal

    @staticmethod
    async def get_board_members(
        board_id: int, requester_email: str
    ) -> list[BoardMemberOutputSchema]:
        """Get all members of a board"""
        # Validate requester has access to board
        await PermissionService.validate_user_board_access(requester_email, board_id)

        # Get board members
        members = await BoardRepository.get_board_members(board_id)

        # Get board owner info
        board = await BoardRepository.get_board_by_identifier(board_id)

        return [
            BoardMemberOutputSchema(
                id=member.id,
                name=member.name,
                surname=member.surname,
                email=member.email,
                is_owner=member.id == board.owner_id,
            )
            for member in members
        ]
