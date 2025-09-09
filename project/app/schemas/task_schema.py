from datetime import datetime

from pydantic import Field

from app.schemas.base_schema import BaseSchema


# Input schema (user does not provide order)
class TaskInputSchema(BaseSchema):
    title: str
    description: str
    column_id: int


# Create schema (service adds order)
class TaskCreateSchema(TaskInputSchema):
    order: int


# Output schema
class TaskOutputSchema(TaskCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskFilterByTitleAndBoard(BaseSchema):
    title: str
    board_id: int


class TaskUpdateOrderSchema(BaseSchema):
    id: int
    new_order: int = Field(ge=0)
