from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace_schema import WorkspaceInputSchema, WorkspaceOutputSchema, WorkspaceCreateSchema, \
    WorkspaceFilterInputSchema, WorkspaceFilterByUserInputSchema
from app.services.user_service.user_service import UserService
from app.services.workspace_service.workspace_service_exception import WorkspaceServiceExceptionInfo, \
    WorkspaceServiceException


class WorkspaceService:
    @staticmethod
    async def create_workspace(workspace: WorkspaceInputSchema, user_email) -> WorkspaceOutputSchema:
        user_model = await UserService.get_user_by_email(user_email)

        # Check user not contain workspace with equals name
        workspace_equals = WorkspaceService.get_workspace_by_name(
            WorkspaceFilterInputSchema(name=workspace.name, owner_id=user_model.id))

        if workspace_equals:
            raise WorkspaceServiceException(WorkspaceServiceExceptionInfo.ERROR_EXISTING_WORKSPACE)

        workspace_complete = WorkspaceCreateSchema(**workspace.model_dump(), owner_id=user_model.id)

        response = await WorkspaceRepository.create_workspace(workspace_complete.model_dump())
        if not response:
            raise WorkspaceServiceException(WorkspaceServiceExceptionInfo.ERROR_CREATING_WORKSPACE)

        await response.user.add(user_model)

        return WorkspaceOutputSchema(**response.__dict__)

    @staticmethod
    async def get_workspace_by_name(workspace_filtered: WorkspaceFilterInputSchema) -> WorkspaceOutputSchema | None:
        print(workspace_filtered)
        return await WorkspaceRepository.get_workspace_by_name(workspace_filtered.model_dump())

    @staticmethod
    async def check_user_contain_workspace(payload: WorkspaceFilterByUserInputSchema) -> bool:
        return True if await WorkspaceRepository.check_user_contain_workspace(payload.model_dump()) else False
