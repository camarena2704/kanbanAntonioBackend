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
    """
    Retrieve all columns for a specific board.

    Returns a list of columns in the specified board ordered by their position.
    Only board members can access this information.

    Parameters:
    - board_id: ID of the board to get columns from
    - auth_data: Authentication data containing user information

    Returns:
    - List of column objects with their details
    """
    user_email = auth_data.payload.get("email")
    return await ColumnService.get_all_columns_by_board_id(board_id, user_email)


@router.post("/", response_model=ColumnOutputSchema)
async def create_column(
    column: ColumnInputSchema, auth_data: AuthDataOutputSchema = Depends(decode_token)
) -> ColumnOutputSchema:
    """
    Create a new column in a board.

    Creates a new column in the specified board with the provided name.
    The column is added at the end of the existing columns.
    Only board members can create columns.

    Parameters:
    - column: Column creation data including name and board ID
    - auth_data: Authentication data containing user information

    Returns:
    - The created column object with its details
    """
    user_email = auth_data.payload.get("email")
    return await ColumnService.create_column(column, user_email)


@router.put("/change-name", response_model=ColumnOutputSchema)
async def update_column_name(
    column: ColumnUpdateNameSchema,
    auth_data: AuthDataOutputSchema = Depends(decode_token),
) -> ColumnOutputSchema:
    """
    Update the name of a column.

    Changes the name of an existing column.
    Only board members can update column names.

    Parameters:
    - column: Contains column ID and the new name
    - auth_data: Authentication data containing user information

    Returns:
    - The updated column object with its details
    """
    user_email = auth_data.payload.get("email")
    return await ColumnService.update_column_name(column, user_email)


@router.put("/move", response_model=ColumnOutputSchema)
async def move_column(
    column_info: ColumnUpdateOrderSchema,
    auth_data: AuthDataOutputSchema = Depends(decode_token),
) -> ColumnOutputSchema:
    """
    Change the position of a column within a board.

    Moves a column to a new position, adjusting the positions of other columns
    as needed.
    Only board members can move columns.

    Parameters:
    - column_info: Contains column ID and the new position
    - auth_data: Authentication data containing user information

    Returns:
    - The moved column object with its updated details
    """
    user_email = auth_data.payload.get("email")
    return await ColumnService.move_column(column_info, user_email)


@router.delete("/{column_id}", response_model=ColumnOutputSchema)
async def delete_column(
    column_id: int, auth_data: AuthDataOutputSchema = Depends(decode_token)
) -> ColumnOutputSchema:
    """
    Delete a column from a board.

    Permanently removes a column and all its associated tasks.
    Only board members can delete columns.

    Parameters:
    - column_id: ID of the column to delete
    - auth_data: Authentication data containing user information

    Returns:
    - The deleted column object with its details
    """
    user_email = auth_data.payload.get("email")
    return await ColumnService.delete_column(column_id, user_email)
