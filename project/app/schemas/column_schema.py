from app.schemas.base_schema import BaseSchema


class ColumnCreateSchema(BaseSchema):
    name: str
    order: int
    board_id: int


class ColumnOutputSchema(ColumnCreateSchema):
    id: int
