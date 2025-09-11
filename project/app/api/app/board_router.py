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
    user_email = token.payload.get("email")
    return await BoardService.get_all_board_paginate_by_workspace_id(
        user_email, workspace_id, is_favourite, page, limit
    )


@router.get("/{board_id}/members", response_model=list[BoardMemberOutputSchema])
async def get_board_members(
    board_id: int,
    token: AuthDataOutputSchema = Depends(decode_token),
) -> list[BoardMemberOutputSchema]:
    user_email = token.payload.get("email")
    return await BoardService.get_board_members(board_id, user_email)


@router.post("/", response_model=BoardOutputSchema)
async def create_board(
    payload: BoardCreateSchema,
    token_decoder: AuthDataOutputSchema = Depends(decode_token),
) -> BoardOutputSchema:
    user_email = token_decoder.payload.get("email")
    return await BoardService.create_board(payload, user_email)


@router.post("/invite", response_model=BoardInvitationSchema)
async def invite_user_to_board(
    invitation: BoardInvitationSchema,
    token: AuthDataOutputSchema = Depends(decode_token),
) -> BoardInvitationSchema:
    user_email = token.payload.get("email")
    return await BoardService.invite_user_to_board(invitation, user_email)


@router.put("/update-favorite/{board_id}", response_model=BoardOutputSchema)
async def update_board_favourite(
    board_id: int, token: AuthDataOutputSchema = Depends(decode_token)
) -> BoardOutputSchema:
    return await BoardService.update_favorite_board(
        board_id, token.payload.get("email")
    )


@router.delete("/remove-member", response_model=BoardRemoveMemberSchema)
async def remove_user_from_board(
    removal: BoardRemoveMemberSchema,
    token: AuthDataOutputSchema = Depends(decode_token),
) -> BoardRemoveMemberSchema:
    user_email = token.payload.get("email")
    return await BoardService.remove_user_from_board(removal, user_email)
