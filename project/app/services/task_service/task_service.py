from black.trans import defaultdict

from app.repositories.column_repository import ColumnRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.column_schema import (
    ColumnOutputSchema,
    ColumnWithTasksSchema,
)
from app.schemas.task_schema import (
    TaskCreateSchema,
    TaskFilterByTitleAndBoard,
    TaskInputSchema,
    TaskOutputSchema,
    TaskUpdateOrderSchema,
    TaskUpdateSchema,
)
from app.services.column_service.column_service import ColumnService
from app.services.permission_service.permission_service import PermissionService
from app.services.task_service.task_service_exception import (
    TaskServiceException,
    TaskServiceExceptionInfo,
)
from app.utils.string_helper import StringHelper


class TaskService:
    @staticmethod
    async def create_task(task: TaskInputSchema, user_email: str) -> TaskOutputSchema:
        # Validate user has permission to create tasks in this column
        await PermissionService.validate_user_column_access(user_email, task.column_id)

        # get board_id from column
        column = await ColumnService.get_column_by_id(task.column_id)
        board_id = column.board_id

        # check if task with same title exists in board
        is_exist = await TaskService.get_task_by_title_and_board_id(
            TaskFilterByTitleAndBoard(
                title=task.title,
                board_id=board_id,
            )
        )
        if is_exist:
            raise TaskServiceException(
                TaskServiceExceptionInfo.ERROR_EXISTING_TASK_IN_BOARD
            )

        # calculate next order automatically via repository
        next_order = await TaskRepository.get_next_order_by_column_id(task.column_id)

        # create schema for insertion
        task_create = TaskCreateSchema(**task.model_dump(), order=next_order)

        response = await TaskRepository.create_task(task_create.model_dump())
        if not response:
            raise TaskServiceException(TaskServiceExceptionInfo.ERROR_CREATING_TASK)

        return TaskOutputSchema(**response.__dict__)

    @staticmethod
    async def get_task_by_title_and_board_id(
        task_filter: TaskFilterByTitleAndBoard,
    ) -> TaskOutputSchema | None:
        return await TaskRepository.get_task_by_title_and_board_id(
            TaskFilterByTitleAndBoard(
                board_id=task_filter.board_id, title=task_filter.title.strip()
            ).model_dump()
        )

    @staticmethod
    async def get_columns_with_tasks(
        board_id: int, user_email: str
    ) -> list[ColumnWithTasksSchema]:
        # Validate user has access to this board
        await PermissionService.validate_user_board_access(user_email, board_id)

        # get all columns for board
        columns = await ColumnRepository.get_all_column_by_board_id(board_id)
        if not columns:
            return []

        # get all tasks for board in one query
        tasks = await TaskRepository.get_all_tasks_by_board_id(board_id)

        # group tasks by column_id
        tasks_by_column = defaultdict(list)
        for task in tasks:
            tasks_by_column[task.column_id].append(TaskOutputSchema(**task.__dict__))

        # build response
        result = []
        for column in columns:
            result.append(
                ColumnWithTasksSchema(
                    **ColumnOutputSchema(**column.__dict__).model_dump(),
                    tasks=tasks_by_column.get(column.id, []),
                )
            )

        return result

    @staticmethod
    async def get_task_by_id(task_id: int) -> TaskOutputSchema:
        response = await TaskRepository.get_task_by_id(task_id)
        if not response:
            raise TaskServiceException(TaskServiceExceptionInfo.ERROR_TASK_NOT_FOUND)
        return TaskOutputSchema(**response.__dict__)

    @staticmethod
    async def move_task(
        update_task: TaskUpdateOrderSchema, user_email: str
    ) -> TaskOutputSchema:
        # Validate user has permission to modify this task
        await PermissionService.validate_user_task_access(user_email, update_task.id)

        # Validate exist column with id
        await ColumnService.get_column_by_id(update_task.column_id)

        task = await TaskService.get_task_by_id(update_task.id)
        updated_task = await TaskRepository.update_order_task(
            {
                "order": task.order,
                "task_id": task.id,
                "new_order": update_task.new_order,
                "column_id": update_task.column_id,
            }
        )
        if not updated_task:
            raise TaskServiceException(TaskServiceExceptionInfo.ERROR_UPDATING_TASK)

        return TaskOutputSchema(**updated_task.__dict__)

    @staticmethod
    async def delete_task(task_id: int, user_email: str) -> TaskOutputSchema:
        # Validate user has permission to delete this task
        await PermissionService.validate_user_task_access(user_email, task_id)

        await TaskService.get_task_by_id(task_id)
        response = await TaskRepository.delete_task(task_id)

        if not response:
            raise TaskServiceException(TaskServiceExceptionInfo.ERROR_DELETING_TASK)

        return TaskOutputSchema(**response.__dict__)

    @staticmethod
    async def update_task(
        task_schema: TaskUpdateSchema, user_email: str
    ) -> TaskOutputSchema:
        # Validate user has permission to update this task
        await PermissionService.validate_user_task_access(user_email, task_schema.id)

        task = await TaskService.get_task_by_id(task_schema.id)

        title = StringHelper.normalize_and_validate(task_schema.title)
        if title:
            column = await ColumnService.get_column_by_id(task.column_id)
            board_id = column.board_id
            task_aux = await TaskService.get_task_by_title_and_board_id(
                TaskFilterByTitleAndBoard(title=title, board_id=board_id)
            )

            if task_aux:
                raise TaskServiceException(
                    TaskServiceExceptionInfo.ERROR_EXISTING_TASK_IN_BOARD
                )
        else:
            title = task.title

        description = (
            StringHelper.normalize_and_validate(task_schema.description)
            or task.description
        )

        task_normalize_data = TaskUpdateSchema(
            id=task.id,
            title=title,
            description=description,
        )

        response = await TaskRepository.update_task(task_normalize_data.model_dump())

        if not response:
            raise TaskServiceException(TaskServiceExceptionInfo.ERROR_UPDATING_TASK)

        return TaskOutputSchema(**response.__dict__)
