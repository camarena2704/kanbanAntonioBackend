import os
from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from app.repositories.token_repository import TokenRepository

from app.modules.database_module.models.default.token import Token  # Tu modelo ORM de Token

import os

from app.schemas.auth_schema import AuthDataOutputSchema

security = HTTPBearer()

JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> AuthDataOutputSchema:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience="messaging_app_client",
            issuer="messaging_backend"
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: no subject")

        return AuthDataOutputSchema(token=token, payload=payload)

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
