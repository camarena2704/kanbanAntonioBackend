from datetime import datetime

from app.schemas.base_schema import BaseSchema


class TaskCreateSchema(BaseSchema):
    title: str
    description: str
    order: int
    column_id: int

class TaskOutputSchema(TaskCreateSchema):
    created_at: datetime
    updated_at: datetime


class TaskFilterByTitleAndBoard(BaseSchema):
    title: str
    board_id: int
