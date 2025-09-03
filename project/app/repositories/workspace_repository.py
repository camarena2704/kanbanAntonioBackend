from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Workspace


class WorkspaceRepository:
    @staticmethod
    async def create_workspace(payload: dict) -> Workspace | None:
        return await DatabaseModule.post_entity(Workspace, payload)

    @staticmethod
    async def get_workspace_by_name(payload: dict) -> Workspace | None:
        return await DatabaseModule.get_entity_filtered(
            Workspace,
            {"name__iexact": payload.get("name"), "owner_id": payload.get("owner_id")},
        )

    @staticmethod
    async def check_user_contain_workspace(payload: dict) -> Workspace | None:
        return await DatabaseModule.get_entity_filtered(
            Workspace,
            {"id": payload.get("workspace_id"), "user__id": payload.get("user_id")},
        )

    @staticmethod
    async def get_all_workspace(user_email: str) -> list[Workspace] | None:
        return await DatabaseModule.get_all_entity_filtered(
            Workspace, {"user__email": user_email}
        )
