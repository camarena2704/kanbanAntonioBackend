from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace_schema import (
    WorkspaceCreateSchema,
    WorkspaceFilterByUserIdOutputSchema,
    WorkspaceFilterByUserInputSchema,
    WorkspaceInputSchema,
    WorkspaceInvitationSchema,
    WorkspaceMemberOutputSchema,
    WorkspaceOutputSchema,
    WorkspaceRemoveMemberSchema,
)
from app.services.permission_service.permission_service import PermissionService
from app.services.user_service.user_service import UserService
from app.services.workspace_service.workspace_service_exception import (
    WorkspaceServiceException,
    WorkspaceServiceExceptionInfo,
)


class WorkspaceService:
    @staticmethod
    async def create_workspace(
        workspace: WorkspaceInputSchema, user_email
    ) -> WorkspaceOutputSchema:
        user_model = await UserService.get_user_by_email_model(user_email)
        # Check user not contain workspace with equals name
        workspace_equals = await WorkspaceService.get_workspace_by_name(
            WorkspaceCreateSchema(name=workspace.name.strip(), owner_id=user_model.id)
        )

        if workspace_equals:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_EXISTING_WORKSPACE
            )

        workspace_complete = WorkspaceCreateSchema(
            name=workspace.name.strip(), owner_id=user_model.id
        )

        response = await WorkspaceRepository.create_workspace(
            workspace_complete.model_dump()
        )
        if not response:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_CREATING_WORKSPACE
            )

        await response.user.add(user_model)

        return WorkspaceOutputSchema(**response.__dict__)

    @staticmethod
    async def get_workspace_by_name(
        workspace_filtered: WorkspaceCreateSchema,
    ) -> WorkspaceOutputSchema | None:
        return await WorkspaceRepository.get_workspace_by_name(
            workspace_filtered.model_dump()
        )

    @staticmethod
    async def check_user_contain_workspace(
        payload: WorkspaceFilterByUserInputSchema,
    ) -> bool:
        return (
            True
            if await WorkspaceRepository.check_user_contain_workspace(
                payload.model_dump()
            )
            else False
        )

    @staticmethod
    async def get_all_workspaces(
        user_email: str,
    ) -> list[WorkspaceFilterByUserIdOutputSchema]:
        response = await WorkspaceRepository.get_all_workspace(user_email)
        if not response:
            return []

        return [
            WorkspaceFilterByUserIdOutputSchema(**workspace.__dict__)
            for workspace in response
        ]

    @staticmethod
    async def invite_user_to_workspace(
        invitation: WorkspaceInvitationSchema, inviter_email: str
    ) -> dict:
        """Invite a user to a workspace"""
        # Validate inviter is workspace owner
        await PermissionService.validate_workspace_ownership(
            inviter_email, invitation.workspace_id
        )

        # Get the user being invited
        try:
            invited_user = await UserService.get_user_by_email_model(
                invitation.invited_user_email
            )
        except Exception:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_INVITED_USER_NOT_FOUND
            )

        # Check if user is already in the workspace
        is_already_member = await WorkspaceRepository.check_user_contain_workspace(
            {"workspace_id": invitation.workspace_id, "user_id": invited_user.id}
        )

        if is_already_member:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_USER_ALREADY_IN_WORKSPACE
            )

        # Get workspace and add user
        workspace = await WorkspaceRepository.get_workspace_by_id(
            invitation.workspace_id
        )
        if not workspace:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_WORKSPACE_NOT_FOUND
            )

        # Add user to workspace
        await workspace.user.add(invited_user)

        return {
            "message": f"User {invitation.invited_user_email} "
            f"successfully added to workspace",
            "workspace_id": invitation.workspace_id,
            "user_email": invitation.invited_user_email,
        }

    @staticmethod
    async def remove_user_from_workspace(
        removal: WorkspaceRemoveMemberSchema, remover_email: str
    ) -> dict:
        """Remove a user from a workspace"""
        # Validate remover is workspace owner
        await PermissionService.validate_workspace_ownership(
            remover_email, removal.workspace_id
        )

        # Get the user being removed
        try:
            user_to_remove = await UserService.get_user_by_email_model(
                removal.user_email_to_remove
            )
        except Exception:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_USER_TO_REMOVE_NOT_FOUND
            )

        # Check if user is in the workspace
        is_member = await WorkspaceRepository.check_user_contain_workspace(
            {"workspace_id": removal.workspace_id, "user_id": user_to_remove.id}
        )

        if not is_member:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_USER_NOT_IN_WORKSPACE
            )

        # Prevent removing the workspace owner
        workspace = await WorkspaceRepository.get_workspace_by_id(removal.workspace_id)
        if workspace.owner_id == user_to_remove.id:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_CANNOT_REMOVE_WORKSPACE_OWNER
            )

        # Remove user from workspace
        await workspace.user.remove(user_to_remove)

        return {
            "message": f"User {removal.user_email_to_remove} "
            f"successfully removed from workspace",
            "workspace_id": removal.workspace_id,
            "user_email": removal.user_email_to_remove,
        }

    @staticmethod
    async def get_workspace_members(
        workspace_id: int, requester_email: str
    ) -> list[WorkspaceMemberOutputSchema]:
        """Get all members of a workspace"""
        # Validate requester has access to workspace
        await PermissionService.validate_user_workspace_access(
            requester_email, workspace_id
        )

        # Get workspace members
        members = await WorkspaceRepository.get_workspace_members(workspace_id)

        # Get workspace owner info
        workspace = await WorkspaceRepository.get_workspace_by_id(workspace_id)
        if not workspace:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_WORKSPACE_NOT_FOUND
            )

        return [
            WorkspaceMemberOutputSchema(
                id=member.id,
                name=member.name,
                surname=member.surname,
                email=member.email,
                is_owner=member.id == workspace.owner_id,
            )
            for member in members
        ]

    @staticmethod
    async def delete_workspace(
        workspace_id: int, requester_email: str
    ) -> WorkspaceOutputSchema:
        """Delete a workspace (only workspace owner can do this)"""
        # Validate requester is workspace owner
        await PermissionService.validate_workspace_ownership(
            requester_email, workspace_id
        )

        # Get workspace to return info before deletion
        workspace = await WorkspaceRepository.get_workspace_by_id(workspace_id)
        if not workspace:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_WORKSPACE_NOT_FOUND
            )

        # Delete workspace (this will cascade delete all boards, columns, tasks)
        deleted_workspace = await WorkspaceRepository.delete_workspace(workspace_id)

        if not deleted_workspace:
            raise WorkspaceServiceException(
                WorkspaceServiceExceptionInfo.ERROR_DELETING_WORKSPACE
            )

        return WorkspaceOutputSchema(**deleted_workspace.__dict__)
