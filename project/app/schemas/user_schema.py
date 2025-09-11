from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserInputSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None

class UserOutputSchema(UserInputSchema):
    id: int
    created_at: datetime
    updated_at: datetime
