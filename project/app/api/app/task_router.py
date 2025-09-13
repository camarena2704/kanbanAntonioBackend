from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.column_schema import ColumnWithTasksSchema
from app.schemas.task_schema import (
    TaskInputSchema,
    TaskOutputSchema,
    TaskUpdateOrderSchema,
    TaskUpdateSchema,
)
from app.services.task_service.task_service import TaskService

router = APIRouter()


@router.get("/board/{board_id}", response_model=list[ColumnWithTasksSchema])
async def get_columns_with_tasks(
    board_id: int, auth_data: AuthDataOutputSchema = Depends(decode_token)
):
    """
    Retrieve all columns with their associated tasks for a specific board.

    Returns a hierarchical structure of columns and their tasks for the
    specified board. Only board members can access this information.

    Parameters:
    - board_id: ID of the board to get columns and tasks from
    - auth_data: Authentication data containing user information

    Returns:
    - List of column objects with nested task objects
    """
    user_email = auth_data.payload.get("email")
    return await TaskService.get_columns_with_tasks(board_id, user_email)


@router.post("/", response_model=TaskOutputSchema)
async def create_task(
    task: TaskInputSchema, auth_data: AuthDataOutputSchema = Depends(decode_token)
) -> TaskOutputSchema:
    """
    Create a new task in a column.

    Creates a new task in the specified column with the provided details.
    The task is added at the end of the existing tasks in the column.
    Only board members can create tasks.

    Parameters:
    - task: Task creation data including title, description, and column ID
    - auth_data: Authentication data containing user information

    Returns:
    - The created task object with its details
    """
    user_email = auth_data.payload.get("email")
    return await TaskService.create_task(task, user_email)


@router.put("/update", response_model=TaskOutputSchema)
async def update_task(
    task_info: TaskUpdateSchema, auth_data: AuthDataOutputSchema = Depends(decode_token)
):
    """
    Update the details of a task.

    Modifies an existing task with the provided information.
    Only board members can update tasks.

    Parameters:
    - task_info: Contains task ID and the fields to update (title, description,
      etc.)
    - auth_data: Authentication data containing user information

    Returns:
    - The updated task object with its details
    """
    user_email = auth_data.payload.get("email")
    return await TaskService.update_task(task_info, user_email)


@router.put("/move", response_model=TaskOutputSchema)
async def move_task(
    task_info: TaskUpdateOrderSchema,
    auth_data: AuthDataOutputSchema = Depends(decode_token),
) -> TaskOutputSchema:
    """
    Move a task to a different position or column.

    Changes the position of a task within its column or moves it to a different
    column. Adjusts the positions of other tasks as needed.
    Only board members can move tasks.

    Parameters:
    - task_info: Contains task ID, target column ID, and the new position
    - auth_data: Authentication data containing user information

    Returns:
    - The moved task object with its updated details
    """
    user_email = auth_data.payload.get("email")
    return await TaskService.move_task(task_info, user_email)


@router.delete("/{task_id}", response_model=TaskOutputSchema)
async def delete_task(
    task_id: int, auth_data: AuthDataOutputSchema = Depends(decode_token)
):
    """
    Delete a task.

    Permanently removes a task from its column.
    Only board members can delete tasks.

    Parameters:
    - task_id: ID of the task to delete
    - auth_data: Authentication data containing user information

    Returns:
    - The deleted task object with its details
    """
    user_email = auth_data.payload.get("email")
    return await TaskService.delete_task(task_id, user_email)
