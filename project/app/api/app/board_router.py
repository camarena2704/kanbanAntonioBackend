from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.repositories.board_repository import BoardRepository
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.board_schema import BoardOutputSchema, BoardCreateSchema
from app.services.board_service.board_service import BoardService

router = APIRouter()


@router.post("/", response_model=BoardOutputSchema)
async def create_board(payload: BoardCreateSchema,
                       token_decoder: AuthDataOutputSchema = Depends(decode_token)) -> BoardOutputSchema:
    user_email = token_decoder.payload.get('email')
    return await BoardService.create_board(payload, user_email)
