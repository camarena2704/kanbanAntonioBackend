from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Task, TaskByBoard


class TaskRepository:
    @staticmethod
    async def create_task(payload: dict) -> Task | None:
        return await DatabaseModule.post_entity(Task, payload)

    @staticmethod
    async def get_task_by_title_and_board_id(payload: dict) -> Task | None:
        return await DatabaseModule.get_entity_filtered(TaskByBoard, {
            "title__iexact": payload.get("title"),
            "board_id": payload.get("board_id")
        })
