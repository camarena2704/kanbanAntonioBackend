from app.repositories.board_repository import BoardRepository
from app.schemas.board_schema import BoardCreateSchema, BoardOutputSchema, BoardFilterByNameSchema
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
        is_name_board_exist = await BoardService.get_board_by_name_and_workspace_id(BoardFilterByNameSchema(
            name=board.name,
            workspace_id=board.workspace_id
        ))

        if is_name_board_exist:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_EXISTING_BOARD_IN_WORKSPACE)

        response = await BoardRepository.create_board(board.model_dump())
        if not response:
            raise BoardServiceException(BoardServiceExceptionInfo.ERROR_CREATING_BOARD)
        return BoardOutputSchema(**response.__dict__)

    @staticmethod
    async def get_board_by_name_and_workspace_id(board_filtered: BoardFilterByNameSchema) -> BoardOutputSchema | None:
        return await BoardRepository.get_board_by_name_and_workspace(BoardFilterByNameSchema(
            name=board_filtered.name.strip(),
            workspace_id=board_filtered.workspace_id
        ).model_dump())
