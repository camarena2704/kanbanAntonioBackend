from app.repositories.task_repository import TaskRepository
from app.schemas.task_schema import TaskCreateSchema, TaskOutputSchema, TaskFilterByTitleAndBoard
from app.services.column_service.column_service import ColumnService
from app.services.task_service.task_service_exception import TaskServiceException, TaskServiceExceptionInfo


class TaskService:
    @staticmethod
    async def create_task(task: TaskCreateSchema) -> TaskOutputSchema:
        # check does not exist title task in board
        column = await ColumnService.get_column_by_id(task.column_id)
        board_id = column.board_id

        is_exist = await TaskService.get_task_by_title_and_board_id(
            TaskFilterByTitleAndBoard(
                title=task.title,
                board_id=board_id,
            )
        )

        if is_exist:
            raise TaskServiceException(TaskServiceExceptionInfo.ERROR_EXISTING_TASK_IN_BOARD)

        task_copy = task.model_copy()
        task_copy.title = task.title.strip()
        task_copy.description = task.description.strip()

        response = await TaskRepository.create_task(task_copy.model_dump())

        if not response:
            raise TaskServiceException(TaskServiceExceptionInfo.ERROR_CREATING_TASK)

        return TaskOutputSchema(**response.__dict__)

    @staticmethod
    async def get_task_by_title_and_board_id(task_filter: TaskFilterByTitleAndBoard) -> TaskOutputSchema | None:
        return await TaskRepository.get_task_by_title_and_board_id(
            TaskFilterByTitleAndBoard(
                board_id=task_filter.board_id,
                title=task_filter.title.strip()
            ).model_dump()
        )
