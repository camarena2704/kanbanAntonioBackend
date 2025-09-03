from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Column


class ColumnRepository:
    @staticmethod
    async def create_column(payload: dict) -> Column | None:
        return await DatabaseModule.post_entity(Column, payload)

    @staticmethod
    async def get_column_by_name_and_board_id(payload: dict) -> Column | None:
        return await DatabaseModule.get_entity_filtered(
            Column,
            {"name__iexact": payload.get("name"), "board_id": payload.get("board_id")},
        )

    @staticmethod
    async def get_column_by_id(column_id: int) -> Column | None:
        return await DatabaseModule.get_entity(Column, column_id)
