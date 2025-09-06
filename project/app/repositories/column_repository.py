from tortoise.expressions import F
from tortoise.functions import Max

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

    @staticmethod
    async def get_all_column_by_board_id(board_id: int) -> list[Column] | None:
        return await DatabaseModule.get_all_entity_filtered(
            Column, {"board_id": board_id}
        )

    @staticmethod
    async def get_next_order_by_board_id(board_id: int) -> int:
        # Get the maximum order in the board
        result = (
            await Column.filter(board_id=board_id)
            .annotate(max_order=Max("order"))
            .values("max_order")
        )
        max_order = (
            result[0]["max_order"]
            if result and result[0]["max_order"] is not None
            else 0
        )
        return max_order + 1

    @staticmethod
    async def update_column_order(payload: dict) -> Column | None:
        old_order = payload.get("order")
        new_order = payload.get("new_order")
        column_id = payload.get("column_id")
        board_id = payload.get("board_id")
        if new_order < old_order:
            await Column.filter(
                board_id=board_id,
                order__gte=new_order,
                order__lt=old_order,
            ).update(order=F("order") + 1)
        elif new_order > old_order:
            await Column.filter(
                board_id=board_id,
                order__lte=new_order,
                order__gt=old_order,
            ).update(order=F("order") - 1)

        return await DatabaseModule.put_entity(Column, {"order": new_order}, column_id)
