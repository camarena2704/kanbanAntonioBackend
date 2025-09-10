from tortoise.expressions import Q

from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.default import Board, User


class BoardRepository:
    @staticmethod
    async def create_board(payload: dict) -> Board | None:
        return await DatabaseModule.post_entity(Board, payload)

    @staticmethod
    async def get_board_by_name_and_workspace(payload: dict) -> Board | None:
        return await DatabaseModule.get_entity_filtered(
            Board,
            {
                "name__iexact": payload.get("name"),
                "workspace_id": payload.get("workspace_id"),
            },
        )

    @staticmethod
    async def get_all_board_filter_paginate_by_workspace_id(
        filters: dict,
        page: int,
        limit: int,
        query: Q = None,
        order: str = "updated_at",
        exclude: dict = None,
    ) -> tuple[list[Board], int] | None:
        return await DatabaseModule.get_all_entity_filtered_paginated(
            Board,
            q=query,
            filters=filters,
            page=page,
            limit=limit,
            order=order,
            exclude=exclude,
        )

    @staticmethod
    async def get_non_favorite_boards_paginated(
        workspace_id: int,
        user_id: int,
        page: int,
        limit: int,
        order: str = "updated_at",
    ) -> tuple[list[Board], int] | None:
        """Get all boards in workspace that are NOT favorites for the specified user"""

        # Get favorite board IDs for this user in this workspace
        favorite_board_ids = await Board.filter(
            workspace_id=workspace_id, users__id=user_id
        ).values_list("id", flat=True)

        # Filter out favorites
        if favorite_board_ids:
            boards = await DatabaseModule.get_all_entity_filtered_paginated(
                Board,
                page=page,
                limit=limit,
                filters={"workspace_id": workspace_id},
                exclude={"id__in": favorite_board_ids},
            )
            return boards
        else:
            return await DatabaseModule.get_all_entity_filtered_paginated(
                Board,
                page=page,
                limit=limit,
                order=order,
                filters={"workspace_id": workspace_id},
            )

    @staticmethod
    async def put_board(payload: dict, identifier: int) -> Board | None:
        return await DatabaseModule.put_entity(Board, payload, identifier)

    @staticmethod
    async def get_board_by_identifier(identifier: int) -> Board | None:
        return await DatabaseModule.get_entity(Board, identifier)

    @staticmethod
    async def is_favorite_board(board_id: int, user_id: int) -> bool:
        return await Board.filter(id=board_id, users__id=user_id).exists()

    @staticmethod
    async def add_user_to_favorites(board: Board, user: User) -> None:
        await board.users.add(user)

    @staticmethod
    async def remove_user_from_favorites(board: Board, user: User) -> None:
        await board.users.remove(user)
