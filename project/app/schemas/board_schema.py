from datetime import datetime
from typing import Optional

from app.schemas.base_schema import BaseSchema


class BoardCreateSchema(BaseSchema):
    name: str
    is_favourite: Optional[bool] = False
    workspace_id: int


class BoardOutputSchema(BoardCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime
