from fastapi import APIRouter
from fastapi.params import Depends

from app.core.security.decode_token import decode_token
from app.schemas.column_schema import ColumnCreateSchema, ColumnOutputSchema
from app.services.column_service.column_service import ColumnService

router = APIRouter()


@router.post("/", response_model=ColumnOutputSchema)
async def create_column(
    column: ColumnCreateSchema, _=Depends(decode_token)
) -> ColumnOutputSchema:
    return await ColumnService.create_column(column)

@router.get("/{board_id}", response_model=list[ColumnOutputSchema])
async def get_all_columns(board_id: int) -> list[ColumnOutputSchema]:
    return await ColumnService.get_all_columns_by_board_id(board_id)