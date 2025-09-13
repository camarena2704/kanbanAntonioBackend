from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.board_schema import (
    BoardCreateSchema,
    BoardInvitationSchema,
    BoardMemberOutputSchema,
    BoardOutputSchema,
    BoardPaginateSchema,
    BoardRemoveMemberSchema,
)
from app.services.board_service.board_service import BoardService

router = APIRouter()


@router.get("/all-board-paginated/{workspace_id}", response_model=BoardPaginateSchema)
async def get_all_board_paginated(
    workspace_id: int,
    is_favourite: bool = False,
    page: int = 0,
    limit: int = 25,
    token: AuthDataOutputSchema = Depends(decode_token),
) -> BoardPaginateSchema:
    """
    Retrieve paginated boards for a specific workspace.

    Returns a paginated list of boards in the specified workspace.
    Can filter by favorite status and supports pagination parameters.
    Only workspace members can access this information.

    Parameters:
    - workspace_id: ID of the workspace to get boards from
    - is_favourite: Filter for favorite boards only when true
    - page: Page number for pagination (zero-indexed)
    - limit: Maximum number of boards per page
    - token: Authentication data containing user information

    Returns:
    - Paginated board data including total count and board objects
    """
    user_email = token.payload.get("email")
    return await BoardService.get_all_board_paginate_by_workspace_id(
        user_email, workspace_id, is_favourite, page, limit
    )


@router.get("/{board_id}/members", response_model=list[BoardMemberOutputSchema])
async def get_board_members(
    board_id: int,
    token: AuthDataOutputSchema = Depends(decode_token),
) -> list[BoardMemberOutputSchema]:
    """
    Retrieve all members of a specific board.

    Returns a list of users who have access to the specified board.
    Only board members can access this information.

    Parameters:
    - board_id: ID of the board to get members from
    - token: Authentication data containing user information

    Returns:
    - List of board member objects with user details and roles
    """
    user_email = token.payload.get("email")
    return await BoardService.get_board_members(board_id, user_email)


@router.post("/", response_model=BoardOutputSchema)
async def create_board(
    payload: BoardCreateSchema,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> BoardOutputSchema:
    """
    Create a new board within a workspace.

    Creates a new board in the specified workspace with the authenticated
    user as the owner.
    The user must be a member of the workspace to create a board.

    Parameters:
    - payload: Board creation data including name, description, and workspace ID
    - token_decoder: Authentication data containing user information

    Returns:
    - The created board object with its details
    """
    user_email = token_decoder.payload.get("email")
    return await BoardService.create_board(payload, user_email)


@router.post("/invite", response_model=BoardInvitationSchema)
async def invite_user_to_board(
    invitation: BoardInvitationSchema,
    token: AuthDataOutputSchema = Depends(decode_token),
) -> BoardInvitationSchema:
    """
    Invite a user to join a board.

    Allows board owners to invite other users to join their board.
    Only the board owner can invite new members.
    The invited user must be a member of the workspace containing the board.

    Parameters:
    - invitation: Contains board ID and email of the user to invite
    - token: Authentication data containing user information

    Returns:
    - The invitation details including status information
    """
    user_email = token.payload.get("email")
    return await BoardService.invite_user_to_board(invitation, user_email)


@router.put("/update-favorite/{board_id}", response_model=BoardOutputSchema)
async def update_board_favourite(
    board_id: int, token: AuthDataOutputSchema = Depends(decode_token)
) -> BoardOutputSchema:
    """
    Toggle the favorite status of a board for the current user.

    Marks or unmarks a board as a favorite for the authenticated user.
    The user must be a member of the board to change its favorite status.

    Parameters:
    - board_id: ID of the board to toggle favorite status
    - token: Authentication data containing user information

    Returns:
    - The updated board object with its details
    """
    return await BoardService.update_favorite_board(
        board_id, token.payload.get("email")
    )


@router.delete("/remove-member", response_model=BoardRemoveMemberSchema)
async def remove_user_from_board(
    removal: BoardRemoveMemberSchema,
    token: AuthDataOutputSchema = Depends(decode_token),
) -> BoardRemoveMemberSchema:
    """
    Remove a user from a board.

    Allows board owners to remove members from their board.
    Only the board owner can remove members.

    Parameters:
    - removal: Contains board ID and email of the user to remove
    - token: Authentication data containing user information

    Returns:
    - The removal details including status information
    """
    user_email = token.payload.get("email")
    return await BoardService.remove_user_from_board(removal, user_email)
