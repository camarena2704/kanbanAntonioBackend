from fastapi import APIRouter, Request
from fastapi.params import Depends

from app.dependencies.auth_dependecies import get_current_user
from app.schemas.auth_schema import TokenOutputSchema, RegisterInputSchema, LoginInputSchema, RefreshTokenInputSchema, \
    AuthDataOutputSchema
from app.services.user_service.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=TokenOutputSchema)
async def register(payload: RegisterInputSchema, request: Request):
    user_agent = request.headers.get("user-agent", "unknown")
    return await AuthService.register(payload, user_agent)


@router.post("/login", response_model=TokenOutputSchema)
async def login(payload: LoginInputSchema, request: Request):
    user_agent = request.headers.get("user-agent", "unknown")
    return await AuthService.login(payload, user_agent)



@router.post("/refresh", response_model=TokenOutputSchema)
async def refresh_token(
    payload: RefreshTokenInputSchema,
    request: Request
):
    user_agent = request.headers.get("user-agent", "unknown")
    return await AuthService.refresh_token(
        refresh_token=payload.refresh_token,
        user_agent=user_agent
    )


@router.get("/me")
async def get_profile(current_user: AuthDataOutputSchema = Depends(get_current_user)):
    return {
        "message": "You are authenticated!",
        "user_id": current_user.payload["sub"],
        "email": current_user.payload.get("email"),
    }
