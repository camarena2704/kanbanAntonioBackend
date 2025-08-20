from tortoise import fields

from app.modules.database_module.models.database_model import DatabaseModel


class User(DatabaseModel):
    name = fields.CharField(max_length=255)
    surname = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

