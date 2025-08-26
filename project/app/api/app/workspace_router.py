from fastapi import APIRouter
from fastapi.params import Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.workspace_schema import WorkspaceOutputSchema, WorkspaceInputSchema, \
    WorkspaceFilterByUserIdOutputSchema
from app.services.workspace_service.workspace_service import WorkspaceService

router = APIRouter()


@router.post("/", response_model=WorkspaceOutputSchema)
async def create_workspace(workspace_input: WorkspaceInputSchema,
                           token_decoder: AuthDataOutputSchema = Depends(decode_token)) -> WorkspaceOutputSchema:
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.create_workspace(workspace_input, user_email)


@router.get("/all-me", response_model=list[WorkspaceFilterByUserIdOutputSchema])
async def get_all_workspaces_me(token_decoder: AuthDataOutputSchema = Depends(decode_token)):
    user_email = token_decoder.payload.get("email")
    return await WorkspaceService.get_all_workspaces(user_email)
