from fastapi import APIRouter
from fastapi.params import Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema

router = APIRouter()


@router.get("/me")
async def get_profile(current_user: AuthDataOutputSchema = Depends(decode_token)):
    return {
        "email": current_user.payload.get("email"),
        "id": current_user.payload.get("sub"),
        "token": current_user.token,
    }
