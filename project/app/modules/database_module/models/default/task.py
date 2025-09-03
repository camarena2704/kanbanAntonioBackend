from tortoise import fields

from app.modules.database_module.models.database_model import DatabaseModel


class Task(DatabaseModel):
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    order = fields.IntField()
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Relation
    column = fields.ForeignKeyField("default.Column", on_delete=fields.CASCADE)
