from typing import Type

from tortoise.expressions import Q

from app.modules.database_module.models.database_model import DatabaseModel


class GenericDao:
    @classmethod
    async def post_entity(
        cls, model: Type[DatabaseModel], data: dict
    ) -> DatabaseModel | None:
        """
        Create an object passed by parameter and return the identifier
        :param model: entity model to create
        :param data: dict with information to create
        :return: Object created
        :rtype: DatabaseModel | None
        """
        return await model.create(**data)

    @classmethod
    async def get_entity(
        cls, model: Type[DatabaseModel], identifier: int, filters: dict = None
    ) -> DatabaseModel | None:
        """
        Get an object and return it
        :param model: entity model to find
        :param identifier: entity model identifier
        :param filters: filters to find the entity
        :return: Result found if exists
        :rtype: DatabaseModel | None
        """
        filters = filters if filters else {}
        return await model.filter(id=identifier).filter(**filters).first()

    @classmethod
    async def get_entity_filtered(
        cls, model: Type[DatabaseModel], filters: dict
    ) -> DatabaseModel | None:
        """
        Query an object with filter and return it
        :param model: entity model to find
        :param filters: filters to find the entity
        :return: Result found if exists
        :rtype: DatabaseModel | None
        """
        return await model.filter(**filters).first()

    @classmethod
    async def get_all_entity_filtered(
        cls, model: Type[DatabaseModel], filters: dict = None, order: str = None
    ) -> list[DatabaseModel] | None:
        filters = filters if filters else {}
        data = model.filter(**filters).all()

        if order:
            data = data.order_by(order)

        return await data

    @classmethod
    async def get_all_entity_filtered_paginated(
            cls,
            model: Type[DatabaseModel],
            page: int = 0,
            limit: int = 25,
            q: Q = None,
            filters: dict = None,
            exclude: dict = None,
            order: str = None,
    ) -> tuple[list[DatabaseModel], int]:
        filters = filters or {}
        exclude = exclude or {}

        data = model.filter(q, **filters) if q else model.filter(**filters)

        if exclude:
            data = data.exclude(**exclude)

        if order:
            data = data.order_by(order)

        return (
            await data.offset(page * limit).limit(limit),
            await data.count()
        )

    @classmethod
    async def put_entity(
        cls,
        model: Type[DatabaseModel],
        data: dict,
        identifier: int,
    ) -> DatabaseModel | None:
        entity = await model.filter(id=identifier).first()
        if not entity:
            return None

        for key, value in data.items():
            setattr(entity, key, value)

        await entity.save()
        return entity

    @classmethod
    async def remove_entity(
        cls, model: Type[DatabaseModel], identifier: int
    ) -> DatabaseModel | None:
        entity = await model.filter(id=identifier).first()
        await model.filter(id=identifier).delete()
        return entity
