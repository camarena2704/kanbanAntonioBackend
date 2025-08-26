from tortoise import fields, models


class TaskByBoard(models.Model):
    board_id = fields.IntField()
    board_name = fields.TextField()
    column_name = fields.TextField()
    task_id = fields.IntField(pk=True)
    title = fields.TextField()
    description = fields.TextField()
    order = fields.IntField()

    class Meta:
        table = "tasks_by_board"
