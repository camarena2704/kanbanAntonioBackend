from tortoise import fields
from tortoise.fields import OnDelete

from app.modules.database_module.models.database_model import DatabaseModel


class Workspace(DatabaseModel):
    name = fields.CharField(max_length=255)
    owner_id = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Relation
    user = fields.ManyToManyField("default.User",
                                  on_delete=OnDelete.CASCADE,
                                  through="workspace_user",
                                  related_name="workspaces")
