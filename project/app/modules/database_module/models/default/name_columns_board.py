from tortoise import fields, models


class NameColumnsBoard(models.Model):
    name = fields.CharField(max_length=255)
    board_id = fields.IntField()
