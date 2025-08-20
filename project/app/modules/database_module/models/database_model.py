from tortoise import fields, models


class DatabaseModel(models.Model):
    id = fields.IntField(primary_key=True)

    class Meta:
        abstract = True
