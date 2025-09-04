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
        # check user_id contain workspace_id
        user = await UserService.get_user_by_email(user_email)
        is_user_contain_workspace = await WorkspaceService.check_user_contain_workspace(
            WorkspaceFilterByUserInputSchema(
                workspace_id=board.workspace_id, user_id=user.id
            )
        )
        if not is_user_contain_workspace:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_NOT_CONTAIN_WORKSPACE
            )

        # Check user not contain board with equals name in workspace
        is_name_board_exist = await BoardService.get_board_by_name_and_workspace_id(
            BoardFilterByNameSchema(name=board.name, workspace_id=board.workspace_id)
        )

        if is_name_board_exist:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_EXISTING_BOARD_IN_WORKSPACE
            )

        correct_board = BoardCreateSchema(
            name=board.name.strip(),
            workspace_id=board.workspace_id,
        )

        response = await BoardRepository.create_board(correct_board.model_dump())
        if not response:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_CREATING_BOARD)

        board_schema: BoardOutputSchema = BoardOutputSchema(**response.__dict__)
        if board.is_favorite:
            await response.users.add(user)
            board_schema.is_favorite = True

        return board_schema

    @staticmethod
    async def get_board_by_name_and_workspace_id(
        board_filtered: BoardFilterByNameSchema,
    ) -> BoardOutputSchema | None:
        return await BoardRepository.get_board_by_name_and_workspace(
            BoardFilterByNameSchema(
                name=board_filtered.name.strip(),
                workspace_id=board_filtered.workspace_id,
            ).model_dump()
        )

    @staticmethod
    async def get_all_board_paginate_by_workspace_id(
        user_email: str,
        workspace_id: int,
        is_favourite: bool,
        page: int = 0,
        limit: int = 25,
    ) -> BoardPaginateSchema:
        # check user contain workspace_id
        user = await UserService.get_user_by_email(user_email)
        is_user_contain_workspace = await WorkspaceService.check_user_contain_workspace(
            WorkspaceFilterByUserInputSchema(workspace_id=workspace_id, user_id=user.id)
        )

        if not is_user_contain_workspace:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_NOT_CONTAIN_WORKSPACE
            )

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

        return BoardPaginateSchema(
            data=[BoardOutputSchema(**board.__dict__) for board in response[0]],
            total=response[1],
        )

    @staticmethod
    async def get_board_by_identifier(board_id: int) -> BoardOutputSchema:
        response = await BoardRepository.get_board_by_identifier(board_id)
        if not response:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_BOARD_NOT_FOUND)
        return BoardOutputSchema(**response.__dict__)

    @staticmethod
    async def update_favorite_board(
        board_id: int, user_email: str
    ) -> BoardOutputSchema:
        # get user
        user = await UserService.get_user_by_email(user_email)

        # check exist board
        board = await BoardRepository.get_board_by_identifier(board_id)
        board_model = BoardOutputSchema(**board.__dict__)
        # check user contain workspace board
        is_user_contain_workspace = await WorkspaceService.check_user_contain_workspace(
            WorkspaceFilterByUserInputSchema(
                workspace_id=board_model.workspace_id, user_id=user.id
            )
        )

        if not is_user_contain_workspace:
            raise BoardServiceException(
                BoardServiceExceptionInfo.ERROR_USER_NOT_CONTAIN_WORKSPACE
            )

        response = await BoardRepository.put_board(
            {
                "is_favorite": False if board_model.is_favorite else True,
            },
            board_id,
        )
        if not response:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_UPDATING_BOARD)

        return BoardOutputSchema(**response.__dict__)

    @staticmethod
    async def is_favorite_board(favorite_schema: BoardFavoriteSchema) -> bool:
        return await BoardRepository.is_favorite_board(favorite_schema.model_dump())
