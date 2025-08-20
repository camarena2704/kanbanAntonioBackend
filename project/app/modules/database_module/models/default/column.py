from tortoise import fields

from app.modules.database_module.models.database_model import DatabaseModel


class Column(DatabaseModel):
    name = fields.CharField(max_length=255)
    order = fields.IntField()

    # Relation
    board = fields.ForeignKeyField("default.Board", on_delete=fields.CASCADE)
    class Meta:
        table = "columns"