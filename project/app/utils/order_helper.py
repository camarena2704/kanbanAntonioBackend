from typing import Type

from tortoise.expressions import F

from app.modules.database_module import DatabaseModule
from app.modules.database_module.models.database_model import DatabaseModel


class OrderHelper:
    @staticmethod
    async def reorder_entity(
        model: Type[DatabaseModel],
        entity_id: int,
        parent_field: str,
        parent_id: int,
        old_order: int,
        new_order: int,
    ) -> DatabaseModel | None:
        filters = {parent_field: parent_id}

        if new_order < old_order:
            await model.filter(
                **filters,
                order__gte=new_order,
                order__lt=old_order,
            ).update(order=F("order") + 1)

        elif new_order > old_order:
            await model.filter(
                **filters,
                order__gt=old_order,
                order__lte=new_order,
            ).update(order=F("order") - 1)

        return await DatabaseModule.put_entity(model, {"order": new_order}, entity_id)
