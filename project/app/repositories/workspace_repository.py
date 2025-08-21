from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Workspace
from app.services.user_service.user_service import UserService


class WorkspaceRepository:
    @staticmethod
    async def create_workspace(payload: dict) -> Workspace | None:

        return await DatabaseModule.post_entity(Workspace, payload)
