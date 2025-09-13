from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.workspace_schema import (
    WorkspaceFilterByUserIdOutputSchema,
    WorkspaceInputSchema,
    WorkspaceInvitationSchema,
    WorkspaceMemberOutputSchema,
    WorkspaceOutputSchema,
    WorkspaceRemoveMemberSchema,
)
from app.services.workspace_service.workspace_service import WorkspaceService

router = APIRouter()


@router.get("/all-me", response_model=list[WorkspaceFilterByUserIdOutputSchema])
async def get_all_workspaces_me(
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
):
    """
    Retrieve all workspaces associated with the authenticated user.

    Returns a list of workspaces where the user is either an owner or a
    member.
    This endpoint requires authentication.

    Parameters:
    - token_decoder: Authentication data containing user information

    Returns:
    - List of workspace objects with their details
    """
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.get_all_workspaces(user_email)


@router.get("/{workspace_id}/members", response_model=list[WorkspaceMemberOutputSchema])
async def get_workspace_members(
    workspace_id: int,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> list[WorkspaceMemberOutputSchema]:
    """
    Retrieve all members of a specific workspace.

    Returns a list of users who are members of the specified workspace.
    Only workspace members can access this information.

    Parameters:
    - workspace_id: ID of the workspace to get members from
    - token_decoder: Authentication data containing user information

    Returns:
    - List of workspace member objects with user details and roles
    """
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.get_workspace_members(workspace_id, user_email)


@router.post("/", response_model=WorkspaceOutputSchema)
async def create_workspace(
    workspace_input: WorkspaceInputSchema,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> WorkspaceOutputSchema:
    """
    Create a new workspace.

    Creates a new workspace with the authenticated user as the owner.
    The owner has full control over the workspace and can invite other users.

    Parameters:
    - workspace_input: Workspace creation data including name and
      description
    - token_decoder: Authentication data containing user information

    Returns:
    - The created workspace object with its details
    """
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.create_workspace(workspace_input, user_email)


@router.post("/invite", response_model=WorkspaceInvitationSchema)
async def invite_user_to_workspace(
    invitation: WorkspaceInvitationSchema,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> WorkspaceInvitationSchema:
    """
    Invite a user to join a workspace.

    Allows workspace owners to invite other users to join their
    workspace.
    Only the workspace owner can invite new members.

    Parameters:
    - invitation: Contains workspace ID and email of the user to invite
    - token_decoder: Authentication data containing user information

    Returns:
    - The invitation details including status information
    """
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.invite_user_to_workspace(invitation, user_email)


@router.delete("/remove-member", response_model=WorkspaceRemoveMemberSchema)
async def remove_user_from_workspace(
    removal: WorkspaceRemoveMemberSchema,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> WorkspaceRemoveMemberSchema:
    """
    Remove a user from a workspace.

    Allows workspace owners to remove members from their workspace.
    Only the workspace owner can remove members.

    Parameters:
    - removal: Contains workspace ID and email of the user to remove
    - token_decoder: Authentication data containing user information

    Returns:
    - The removal details including status information
    """
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.remove_user_from_workspace(removal, user_email)


@router.delete("/remove-workspace/{workspace_id}", response_model=WorkspaceOutputSchema)
async def remove_workspace(
    workspace_id: int, token_decoder: AuthDataOutputSchema = Depends(decode_token)
):
    """
    Delete a workspace.

    Permanently removes a workspace and all its associated data.
    Only the workspace owner can delete a workspace.

    Parameters:
    - workspace_id: ID of the workspace to delete
    - token_decoder: Authentication data containing user information

    Returns:
    - The deleted workspace object with its details
    """
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.delete_workspace(workspace_id, user_email)
