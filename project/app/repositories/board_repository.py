from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Board


class BoardRepository:
    @staticmethod
    async def create_board(payload: dict) -> Board | None:
        return await DatabaseModule.post_entity(Board, payload)

