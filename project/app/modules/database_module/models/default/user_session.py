from tortoise import fields

from app.modules.database_module.models.database_model import DatabaseModel


class UserSession(DatabaseModel):
    user = fields.ForeignKeyField(
        "default.User",
        on_delete=fields.CASCADE,
        related_name="sessions",
    )
    refresh_token = fields.TextField()
    user_agent = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_used_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user_sessions"
        unique_together = ("user", "refresh_token")
