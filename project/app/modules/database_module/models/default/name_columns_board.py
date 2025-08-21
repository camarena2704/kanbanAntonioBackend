from tortoise import fields


class NameColumnsBoard:
    name = fields.CharField(max_length=255)
    board_id = fields.IntField()
