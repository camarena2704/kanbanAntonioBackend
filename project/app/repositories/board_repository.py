from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Board


class BoardRepository:
    @staticmethod
    async def create_board(payload: dict) -> Board | None:
        return await DatabaseModule.post_entity(Board, payload)

    @staticmethod
    async def get_board_by_name_and_workspace(payload: dict) -> Board | None:
        return await DatabaseModule.get_entity_filtered(Board, {
            "name__iexact": payload.get("name"),
            "workspace_id": payload.get("workspace_id"),
        })
