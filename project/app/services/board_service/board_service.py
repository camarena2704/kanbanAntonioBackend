from tortoise.expressions import Q

from app.repositories.board_repository import BoardRepository
from app.schemas.board_schema import (
    BoardCreateSchema,
    BoardFavoriteSchema,
    BoardFilterByNameSchema,
    BoardOutputSchema,
    BoardPaginateSchema,
)
from app.schemas.workspace_schema import WorkspaceFilterByUserInputSchema
from app.services.board_service.board_service_exception import (
    BoardServiceException,
    BoardServiceExceptionInfo,
)
from app.services.user_service.user_service import UserService
from app.services.workspace_service.workspace_service import WorkspaceService


class BoardService:
    @staticmethod
    async def create_board(
        board: BoardCreateSchema, user_email: str
    ) -> BoardOutputSchema:
        # Get user by email
        user = await UserService.get_user_by_email(user_email)

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

        # Create the board
        payload = BoardCreateSchema(
            name=board.name.strip(),
            workspace_id=board.workspace_id,
        ).model_dump()
        board_model = await BoardRepository.create_board(payload)
        if not board_model:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_CREATING_BOARD)

        response = BoardOutputSchema(**board_model.__dict__)

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
        is_favourite: bool,
        page: int = 0,
        limit: int = 25,
    ) -> BoardPaginateSchema:
        # Get user by email
        user = await UserService.get_user_by_email(user_email)

        # Validate that the user belongs to the workspace
        is_user_contain_workspace = await WorkspaceService.check_user_contain_workspace(
            WorkspaceFilterByUserInputSchema(workspace_id=workspace_id, user_id=user.id)
        )
        if not is_user_contain_workspace:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_NOT_CONTAIN_WORKSPACE
            )

        # Retrieve favorite or non-favorite boards
        if is_favourite:
            response = (
                await BoardRepository.get_all_board_filter_paginate_by_workspace_id(
                    {"workspace_id": workspace_id, "users__id": user.id},
                    page,
                    limit,
                )
            )
        else:
            response = (
                await BoardRepository.get_all_board_filter_paginate_by_workspace_id(
                    {"workspace_id": workspace_id},
                    page,
                    limit,
                    query=Q(workspace_id=workspace_id) & ~Q(users__id=user.id),
                )
            )

        if not response:
            return BoardPaginateSchema(total=0, data=[])

        boards = [BoardOutputSchema(**board.__dict__) for board in response[0]]
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
        user = await UserService.get_user_by_email(user_email)

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
