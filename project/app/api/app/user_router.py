from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.user_schema import UserOutputSchema
from app.services.user_service.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserOutputSchema)
async def get_profile(current_user: AuthDataOutputSchema = Depends(decode_token)):
    """
    Get the profile of the currently authenticated user.
    Retrieves the user data from the database using their email.
    """
    return await UserService.get_user_by_email(current_user.payload.get("email"))


@router.put("/me", response_model=UserOutputSchema)
async def update_profile(
    data: dict, current_user: AuthDataOutputSchema = Depends(decode_token)
):
    """
    Update the profile of the currently authenticated user.
    Accepts a dictionary with the fields to update and returns the updated user.
    """
    user_email = current_user.payload.get("email")
    user = await UserService.get_user_by_email(user_email)
    return await UserService.update_user(user.id, data)


@router.delete("/me", response_model=UserOutputSchema)
async def delete_profile(current_user: AuthDataOutputSchema = Depends(decode_token)):
    """
    Delete the currently authenticated user.
    Removes all sessions, deletes the user from Supabase,
    and deletes the local database record.
    """
    user_email = current_user.payload.get("email")
    uid = current_user.payload.get("sub")
    return await UserService.delete_user(uid, user_email)
