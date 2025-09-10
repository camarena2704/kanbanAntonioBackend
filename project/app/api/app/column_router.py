from fastapi import APIRouter, Depends

from app.core.security.decode_token import decode_token
from app.schemas.auth_schema import AuthDataOutputSchema
from app.schemas.column_schema import (
    ColumnInputSchema,
    ColumnOutputSchema,
    ColumnUpdateNameSchema,
    ColumnUpdateOrderSchema,
)
from app.services.column_service.column_service import ColumnService

router = APIRouter()


@router.get("/{board_id}", response_model=list[ColumnOutputSchema])
async def get_all_columns(
    board_id: int, auth_data: AuthDataOutputSchema = Depends(decode_token)
) -> list[ColumnOutputSchema]:
    user_email = auth_data.payload.get("email")
    return await ColumnService.get_all_columns_by_board_id(board_id, user_email)


@router.post("/", response_model=ColumnOutputSchema)
async def create_column(
    column: ColumnInputSchema, auth_data: AuthDataOutputSchema = Depends(decode_token)
) -> ColumnOutputSchema:
    user_email = auth_data.payload.get("email")
    return await ColumnService.create_column(column, user_email)


@router.put("/change-name", response_model=ColumnOutputSchema)
async def update_column_name(
    column: ColumnUpdateNameSchema,
    auth_data: AuthDataOutputSchema = Depends(decode_token),
) -> ColumnOutputSchema:
    user_email = auth_data.payload.get("email")
    return await ColumnService.update_column_name(column, user_email)


@router.put("/move", response_model=ColumnOutputSchema)
async def move_column(
    column_info: ColumnUpdateOrderSchema,
    auth_data: AuthDataOutputSchema = Depends(decode_token),
) -> ColumnOutputSchema:
    user_email = auth_data.payload.get("email")
    return await ColumnService.move_column(column_info, user_email)


@router.delete("/{column_id}", response_model=ColumnOutputSchema)
async def delete_column(
    column_id: int, auth_data: AuthDataOutputSchema = Depends(decode_token)
) -> ColumnOutputSchema:
    user_email = auth_data.payload.get("email")
    return await ColumnService.delete_column(column_id, user_email)
