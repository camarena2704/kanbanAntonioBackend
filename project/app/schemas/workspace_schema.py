from datetime import datetime

from app.schemas.base_schema import BaseSchema


class WorkspaceInputSchema(BaseSchema):
    name: str


class WorkspaceCreateSchema(WorkspaceInputSchema):
    owner_id: int


class WorkspaceOutputSchema(WorkspaceInputSchema):
    id: int
    owner_id: int = None
    created_at: datetime
    updated_at: datetime


class WorkspaceFilterByUserInputSchema(BaseSchema):
    workspace_id: int
    user_id: int


class WorkspaceFilterByUserIdOutputSchema(WorkspaceInputSchema):
    id: int


class WorkspaceInvitationSchema(BaseSchema):
    workspace_id: int
    invited_user_email: str


class WorkspaceRemoveMemberSchema(BaseSchema):
    workspace_id: int
    user_email_to_remove: str


class WorkspaceMemberOutputSchema(BaseSchema):
    id: int
    name: str
    surname: str
    email: str
    is_owner: bool
