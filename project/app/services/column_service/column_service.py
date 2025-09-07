from tortoise.exceptions import IntegrityError

from app.repositories.column_repository import ColumnRepository
from app.schemas.column_schema import (
    ColumnFilterNameAndBoardIdSchema,
    ColumnInputSchema,
    ColumnOutputSchema,
    ColumnUpdateNameSchema,
    ColumnUpdateOrderSchema,
)
from app.services.column_service.column_service_exception import (
    ColumnServiceException,
    ColumnServiceExceptionInfo,
)
from app.utils.string_helper import StringHelper


class ColumnService:
    @staticmethod
    async def create_column(column: ColumnInputSchema) -> ColumnOutputSchema:
        # clean and validate the name
        clean_name = StringHelper.normalize_and_validate(column.name)
        if not clean_name:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_INVALID_COLUMN_NAME
            )

        # check column with same name does not already exist in board
        is_exist = await ColumnService.get_column_by_name_and_board_id(
            ColumnFilterNameAndBoardIdSchema(name=clean_name, board_id=column.board_id)
        )
        if is_exist:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_EXISTING_COLUMN_IN_BOARD
            )

        # get next order automatically
        next_order = await ColumnRepository.get_next_order_by_board_id(column.board_id)

        # create column
        try:
            payload = {
                "name": clean_name,
                "order": next_order,
                "board_id": column.board_id,
            }
            created_column = await ColumnRepository.create_column(payload)
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
        # clean and validate the name
        clean_name = StringHelper.normalize_and_validate(column.name)
        if not clean_name:
            return None

        return await ColumnRepository.get_column_by_name_and_board_id(
            ColumnFilterNameAndBoardIdSchema(
                name=clean_name, board_id=column.board_id
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

    @staticmethod
    async def get_all_columns_by_board_id(
        board_id: int,
    ) -> list[ColumnOutputSchema] | None:
        list_column = await ColumnRepository.get_all_column_by_board_id(board_id)
        columns_output_schema: list[ColumnOutputSchema] = [
            ColumnOutputSchema(**column.__dict__) for column in list_column
        ]

        return columns_output_schema if columns_output_schema else []

    @staticmethod
    async def move_column(update_column: ColumnUpdateOrderSchema) -> ColumnOutputSchema:
        column = await ColumnService.get_column_by_id(update_column.id)
        updated_column = await ColumnRepository.update_column_order(
            {
                "order": column.order,
                "column_id": column.id,
                "new_order": update_column.new_order,
                "board_id": column.board_id,
            }
        )
        if not updated_column:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_UPDATING_COLUMN
            )

        return ColumnOutputSchema(**updated_column.__dict__)

    @staticmethod
    async def update_column_name(
        column_schema: ColumnUpdateNameSchema,
    ) -> ColumnOutputSchema:
        # clean and validate the name
        clean_name = StringHelper.normalize_and_validate(column_schema.new_name)
        if not clean_name:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_INVALID_COLUMN_NAME
            )

        # get current column by ID
        column = await ColumnService.get_column_by_id(column_schema.id)

        # check if the new name already exists in the same board
        is_exist = await ColumnService.get_column_by_name_and_board_id(
            ColumnFilterNameAndBoardIdSchema(name=clean_name, board_id=column.board_id)
        )
        if is_exist:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_EXISTING_COLUMN_IN_BOARD
            )

        # update column name
        response = await ColumnRepository.update_name_column(
            {**column_schema.model_dump(), "new_name": clean_name}
        )

        # check if update failed
        if not response:
            raise ColumnServiceException(
                ColumnServiceExceptionInfo.ERROR_UPDATING_COLUMN
            )

        # return updated column
        return ColumnOutputSchema(**response.__dict__)
