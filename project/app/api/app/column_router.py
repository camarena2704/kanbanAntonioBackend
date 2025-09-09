from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.column_schema import (
    ColumnInputSchema,
    ColumnOutputSchema,
    ColumnUpdateNameSchema,
    ColumnUpdateOrderSchema,
)
from app.services.column_service.column_service import ColumnService

router = APIRouter()


@router.get("/{board_id}", response_model=list[ColumnOutputSchema])
async def get_all_columns(board_id: int) -> list[ColumnOutputSchema]:
    return await ColumnService.get_all_columns_by_board_id(board_id)


@router.post("/", response_model=ColumnOutputSchema)
async def create_column(
    column: ColumnInputSchema, _=Depends(decode_token)
) -> ColumnOutputSchema:
    return await ColumnService.create_column(column)


@router.put("/change-name", response_model=ColumnOutputSchema)
async def update_column_name(
    column: ColumnUpdateNameSchema, _=Depends(decode_token)
) -> ColumnOutputSchema:
    return await ColumnService.update_column_name(column)


@router.put("/move", response_model=ColumnOutputSchema)
async def move_column(
    column_info: ColumnUpdateOrderSchema, _=Depends(decode_token)
) -> ColumnOutputSchema:
    return await ColumnService.move_column(column_info)


@router.delete("/{column_id}", response_model=ColumnOutputSchema)
async def delete_column(column_id: int, _=Depends(decode_token)) -> ColumnOutputSchema:
    return await ColumnService.delete_column(column_id)
