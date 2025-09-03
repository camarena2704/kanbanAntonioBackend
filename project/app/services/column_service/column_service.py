from tortoise.exceptions import IntegrityError

from app.repositories.column_repository import ColumnRepository
from app.schemas.column_schema import (
    ColumnCreateSchema,
    ColumnFilterNameAndBoardIdSchema,
    ColumnOutputSchema,
)
from app.services.column_service.column_service_exception import (
    ColumnServiceException,
    ColumnServiceExceptionInfo,
)


class ColumnService:
    @staticmethod
    async def create_column(column: ColumnCreateSchema) -> ColumnOutputSchema:
        # check does not exist column in board with equals name
        is_exist = await ColumnService.get_column_by_name_and_board_id(
            ColumnFilterNameAndBoardIdSchema(name=column.name, board_id=column.board_id)
        )
        if is_exist:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_EXISTING_COLUMN_IN_BOARD
            )

        # create column
        try:
            correct_column = ColumnCreateSchema(
                name=column.name.strip(),
                order=column.order,
                board_id=column.board_id,
            )
            created_column = await ColumnRepository.create_column(
                correct_column.model_dump()
            )
        except IntegrityError as e:
            if "columns_board_id_fkey" in str(e):
                raise ColumnServiceException(
                    ColumnServiceExceptionInfo.ERROR_CREATING_COLUMN
                )
            raise

        if not created_column:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_CREATING_COLUMN
            )

        return ColumnOutputSchema(**created_column.__dict__)

    @staticmethod
    async def get_column_by_name_and_board_id(
        column: ColumnFilterNameAndBoardIdSchema,
    ) -> ColumnOutputSchema | None:
        return await ColumnRepository.get_column_by_name_and_board_id(
            ColumnFilterNameAndBoardIdSchema(
                name=column.name.strip(), board_id=column.board_id
            ).model_dump()
        )

    @staticmethod
    async def get_column_by_id(column_id: int) -> ColumnOutputSchema:
        response = await ColumnRepository.get_column_by_id(column_id)

        if not response:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_COLUMN_NOT_FOUND
            )

        return ColumnOutputSchema(**response.__dict__)
