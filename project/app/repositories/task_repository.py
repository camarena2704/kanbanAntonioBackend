from tortoise.functions import Max

from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Task
from app.utils.order_helper import OrderHelper


class TaskRepository:
    @staticmethod
    async def create_task(payload: dict) -> Task | None:
        return await DatabaseModule.post_entity(Task, payload)

    @staticmethod
    async def get_task_by_title_and_board_id(payload: dict) -> Task | None:
        return await DatabaseModule.get_entity_filtered(
            Task,
            {
                "title__iexact": payload.get("title"),
                "column__board_id": payload.get("board_id"),
            },
        )

    @staticmethod
    async def get_all_tasks_by_board_id(board_id: int) -> list[Task]:
        return await Task.filter(column__board_id=board_id).prefetch_related("column")

    @staticmethod
    async def get_next_order_by_column_id(column_id: int) -> int:
        result = (
            await Task.filter(column_id=column_id)
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
    async def get_task_by_id(task_id: int) -> Task | None:
        return await DatabaseModule.get_entity_filtered(Task, {"id": task_id})

    @staticmethod
    async def update_order_task(payload: dict) -> Task | None:
        old_order = payload.get("order")
        new_order = payload.get("new_order")
        column_id = payload.get("column_id")
        task_id = payload.get("task_id")
        return await OrderHelper.reorder_entity(
            Task, task_id, "column_id", column_id, old_order, new_order
        )

    @staticmethod
    async def delete_task(task_id: int) -> Task | None:
        return await DatabaseModule.remove_entity(Task, task_id)
