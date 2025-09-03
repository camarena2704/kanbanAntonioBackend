import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from jwt import ExpiredSignatureError

from app.schemas.auth_schema import AuthDataOutputSchema

security = HTTPBearer()

JWT_SECRET = os.getenv("SUPABASE_JWT_TOKEN")
JWT_ALGORITHM = "HS256"


async def decode_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthDataOutputSchema:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience="authenticated"
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject"
            )
        return AuthDataOutputSchema(token=token, payload=payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
