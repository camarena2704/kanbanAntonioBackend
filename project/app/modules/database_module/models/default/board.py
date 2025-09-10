from tortoise import fields

from app.modules.database_module.models.database_model import DatabaseModel


class Board(DatabaseModel):
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Relations
    workspace = fields.ForeignKeyField("default.Workspace", on_delete=fields.CASCADE)
    owner = fields.ForeignKeyField(
        "default.User", on_delete=fields.CASCADE, related_name="owned_boards"
    )

    # Board favorites (existing)
    users = fields.ManyToManyField(
        "default.User",
        through="favorite_board",
        related_name="favorite_boards",
        on_delete=fields.CASCADE,
    )

    # Board members (new)
    members = fields.ManyToManyField(
        "default.User",
        through="board_member",
        related_name="board_memberships",
        on_delete=fields.CASCADE,
    )
