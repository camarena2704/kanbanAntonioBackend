from app.repositories.board_repository import BoardRepository
from app.schemas.board_schema import BoardCreateSchema, BoardOutputSchema
from app.schemas.workspace_schema import WorkspaceFilterByUserInputSchema
from app.services.board_service.board_service_exception import BoardServiceException, BoardServiceExceptionInfo
from app.services.user_service.user_service import UserService
from app.services.workspace_service.workspace_service import WorkspaceService


class BoardService:
    @staticmethod
    async def create_board(board: BoardCreateSchema, user_email: str) -> BoardOutputSchema:
        # check user_id contain workspace_id
        user = await UserService.get_user_by_email(user_email)
        is_user_contain_workspace = await WorkspaceService.check_user_contain_workspace(
            WorkspaceFilterByUserInputSchema(
                workspace_id=board.workspace_id,
                user_id=user.id
            ))
        if not is_user_contain_workspace:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_USER_NOT_CONTAIN_WORKSPACE)

        # Check user not contain board with equals name in workspace
        # todo: tengo que hacerlo
        response = await BoardRepository.create_board(board.model_dump())
        if not response:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_CREATING_BOARD)
        return BoardOutputSchema(**response.__dict__)

# @staticmethod
# async def get_board_by_name(workspace_filtered: WorkspaceFilterInputSchema) -> WorkspaceOutputSchema | None:
#     print(workspace_filtered)
#     return await WorkspaceRepository.get_workspace_by_name(workspace_filtered.model_dump())
