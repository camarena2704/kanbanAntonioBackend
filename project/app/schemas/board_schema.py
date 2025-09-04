from datetime import datetime
from typing import Optional

from app.schemas.base_schema import BaseSchema


class BoardCreateSchema(BaseSchema):
    name: str
    is_favorite: Optional[bool] = False
    workspace_id: int


class BoardOutputSchema(BoardCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class BoardFilterByNameSchema(BaseSchema):
    name: str
    workspace_id: int


class BoardPaginateSchema(BaseSchema):
    data: list[BoardOutputSchema]
    total: int


class BoardFavoriteSchema(BaseSchema):
    board_id: int
    user_id: int
