from typing import Dict, Any

from pydantic import BaseModel


class AuthDataOutputSchema(BaseModel):
    token: str
    payload: Dict[str, Any]
