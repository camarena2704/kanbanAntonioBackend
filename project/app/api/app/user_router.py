from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.user_schema import UserOutputSchema, UserUpdateSchema
from app.services.user_service.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserOutputSchema)
async def get_profile(
    current_user: AuthDataOutputSchema = Depends(decode_token),
) -> UserOutputSchema:
    """
    Get the profile of the currently authenticated user.

    Retrieves the user data from the database using their email
    from the authentication token.

    Parameters:
    - current_user: Authentication data containing user information

    Returns:
    - User object with profile details
    """
    return await UserService.get_user_by_email(current_user.payload.get("email"))


@router.put("/me", response_model=UserOutputSchema)
async def update_profile(
    data: UserUpdateSchema, current_user: AuthDataOutputSchema = Depends(decode_token)
) -> UserOutputSchema:
    """
    Update the profile of the currently authenticated user.

    Accepts a dictionary with the fields to update and returns the updated user.
    Only the authenticated user can update their own profile.

    Parameters:
    - data: User update data containing fields to modify
    - current_user: Authentication data containing user information

    Returns:
    - Updated user object with profile details
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
    This action is permanent and cannot be undone.

    Parameters:
    - current_user: Authentication data containing user information

    Returns:
    - The deleted user object with profile details
    """
    user_email = current_user.payload.get("email")
    uid = current_user.payload.get("sub")
    return await UserService.delete_user(uid, user_email)
