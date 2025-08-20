from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserInputSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr

class UserOutputSchema(UserInputSchema):
    created_at: datetime
    updated_at: datetime
