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
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.get_all_workspaces(user_email)


@router.post("/", response_model=WorkspaceOutputSchema)
async def create_workspace(
    workspace_input: WorkspaceInputSchema,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> WorkspaceOutputSchema:
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.create_workspace(workspace_input, user_email)


@router.post("/invite", response_model=dict)
async def invite_user_to_workspace(
    invitation: WorkspaceInvitationSchema,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> dict:
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.invite_user_to_workspace(invitation, user_email)


@router.delete("/remove-member", response_model=dict)
async def remove_user_from_workspace(
    removal: WorkspaceRemoveMemberSchema,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> dict:
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.remove_user_from_workspace(removal, user_email)


@router.get("/{workspace_id}/members", response_model=list[WorkspaceMemberOutputSchema])
async def get_workspace_members(
    workspace_id: int,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> list[WorkspaceMemberOutputSchema]:
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.get_workspace_members(workspace_id, user_email)
