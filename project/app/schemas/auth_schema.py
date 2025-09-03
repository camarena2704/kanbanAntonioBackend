from typing import Any, Dict

from pydantic import BaseModel


class AuthDataOutputSchema(BaseModel):
    token: str
    payload: Dict[str, Any]
