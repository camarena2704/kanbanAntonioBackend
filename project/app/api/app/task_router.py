from fastapi import APIRouter
from fastapi.params import Depends

from app.core.security.decode_token import decode_token
from app.schemas.task_schema import TaskOutputSchema, TaskCreateSchema
from app.services.task_service.task_service import TaskService

router = APIRouter()


@router.post("/", response_model=TaskOutputSchema)
async def create_task(task: TaskCreateSchema, _=Depends(decode_token)) -> TaskOutputSchema:
    return await TaskService.create_task(task)
