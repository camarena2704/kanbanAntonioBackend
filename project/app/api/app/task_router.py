from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.column_schema import ColumnWithTasksSchema
from app.schemas.task_schema import (
    TaskInputSchema,
    TaskOutputSchema,
    TaskUpdateOrderSchema,
)
from app.services.task_service.task_service import TaskService

router = APIRouter()


@router.post("/", response_model=TaskOutputSchema)
async def create_task(
        task: TaskInputSchema, _=Depends(decode_token)
) -> TaskOutputSchema:
    return await TaskService.create_task(task)


@router.get("/board/{board_id}", response_model=list[ColumnWithTasksSchema])
async def get_columns_with_tasks(board_id: int, _=Depends(decode_token)):
    return await TaskService.get_columns_with_tasks(board_id)


@router.put("/move", response_model=TaskOutputSchema)
async def move_column(
        task_info: TaskUpdateOrderSchema, _=Depends(decode_token)
) -> TaskOutputSchema:
    return await TaskService.move_task(task_info)


@router.delete("/{task_id}", response_model=TaskOutputSchema)
async def delete_task(task_id: int, _=Depends(decode_token)):
    return await TaskService.delete_task(task_id)
