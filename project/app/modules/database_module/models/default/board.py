from tortoise import fields

from app.modules.database_module.models.database_model import DatabaseModel


class Board(DatabaseModel):
    name = fields.CharField(max_length=255)
    is_favorite = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Relation
    workspace = fields.ForeignKeyField("default.Workspace", on_delete=fields.CASCADE)
