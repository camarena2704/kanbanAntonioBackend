from app.schemas.base_schema import BaseSchema
from app.schemas.task_schema import TaskOutputSchema


class ColumnCreateSchema(BaseSchema):
    name: str
    order: int
    board_id: int


class ColumnOutputSchema(ColumnCreateSchema):
    id: int


class ColumnWithTasksSchema(ColumnOutputSchema):
    tasks: list[TaskOutputSchema]


class ColumnFilterNameAndBoardIdSchema(BaseSchema):
    name: str
    board_id: int
