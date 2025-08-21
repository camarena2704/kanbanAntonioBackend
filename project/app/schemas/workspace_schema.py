from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from app.schemas.base_schema import BaseSchema
from app.schemas.user_schema import UserOutputSchema


class WorkspaceInputSchema(BaseSchema):
    name: str


class WorkspaceCreateSchema(WorkspaceInputSchema):
    user_email: EmailStr
    owner_id: Optional[int] = None
    user: Optional[UserOutputSchema] = None

class WorkspaceOutputSchema(WorkspaceInputSchema):
    id: int
    owner_id: int = None
    created_at: datetime
    updated_at: datetime