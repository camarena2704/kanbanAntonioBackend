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
    user_email = auth_data.payload.get("email")
    return await TaskService.get_columns_with_tasks(board_id, user_email)


@router.post("/", response_model=TaskOutputSchema)
async def create_task(
    task: TaskInputSchema, auth_data: AuthDataOutputSchema = Depends(decode_token)
) -> TaskOutputSchema:
    user_email = auth_data.payload.get("email")
    return await TaskService.create_task(task, user_email)


@router.put("/update", response_model=TaskOutputSchema)
async def update_task(
    task_info: TaskUpdateSchema, auth_data: AuthDataOutputSchema = Depends(decode_token)
):
    user_email = auth_data.payload.get("email")
    return await TaskService.update_task(task_info, user_email)


@router.put("/move", response_model=TaskOutputSchema)
async def move_task(
    task_info: TaskUpdateOrderSchema,
    auth_data: AuthDataOutputSchema = Depends(decode_token),
) -> TaskOutputSchema:
    user_email = auth_data.payload.get("email")
    return await TaskService.move_task(task_info, user_email)


@router.delete("/{task_id}", response_model=TaskOutputSchema)
async def delete_task(
    task_id: int, auth_data: AuthDataOutputSchema = Depends(decode_token)
):
    user_email = auth_data.payload.get("email")
    return await TaskService.delete_task(task_id, user_email)
