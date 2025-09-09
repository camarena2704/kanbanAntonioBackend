from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.user_schema import UserInputSchema, UserOutputSchema
from app.services.user_service.user_service import UserService

router = APIRouter()


@router.get("/me")
async def get_profile(current_user: AuthDataOutputSchema = Depends(decode_token)):
    return {
        "email": current_user.payload.get("email"),
        "id": current_user.payload.get("sub"),
        "token": current_user.token,
    }


@router.post("/register", response_model=UserOutputSchema)
async def register(
    user: UserInputSchema, _: AuthDataOutputSchema = Depends(decode_token)
) -> UserOutputSchema:
    return await UserService.create_user(user)
