from app.schemas.base_schema import BaseSchema


class AuthDataOutputSchema(BaseSchema):
    token: str
    payload: dict
