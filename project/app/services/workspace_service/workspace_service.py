from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace_schema import WorkspaceInputSchema, WorkspaceOutputSchema
from app.services.user_service.user_service import UserService
from app.services.workspace_service.workspace_service_exception import WorkspaceServiceExceptionInfo, \
    WorkspaceServiceException


class WorkspaceService:
    @staticmethod
    async def create_workspace(workspace: WorkspaceInputSchema, user_email) -> WorkspaceOutputSchema:
        user_model = await UserService.get_user_by_email(user_email)
        response = await WorkspaceRepository.create_workspace(workspace.model_dump())
        if not response:
            raise WorkspaceServiceException(WorkspaceServiceExceptionInfo.ERROR_CREATING_WORKSPACE)

        await response.user.add(user_model)

        return WorkspaceOutputSchema(**response.__dict__)
