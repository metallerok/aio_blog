from typing import List, Any
from sqlalchemy import func, Table
from sqlalchemy.orm import Query
from uuid import UUID
from enum import Enum

from math import ceil

DEFAULT_PAGE_SIZE = 20


class Pagination:

    def __init__(self, items: List[Any], total: int, page: int, page_size: int):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size

    @property
    def total_pages(self) -> int:
        return ceil(self.total / self.page_size) or 1


async def paginate(conn, query, page, page_size):
    selectable = query.limit(page_size).offset(
        (page - 1) * page_size
    )

    cursor = await conn.execute(selectable)

    return await cursor.fetchall()


def with_pagination_meta(items: List[Any], pagination: Pagination):
    return {
        'data': items,
        'meta': {
            'current_page': pagination.page,
            'total_pages': pagination.total_pages,
            'page_size': pagination.page_size
        }
    }


class SaQuery:

    filter_field = None
    desc = False

    @classmethod
    async def _get_paginated_items(
            cls, conn, query: Query, page: int, page_size: int
    ) -> List['Table']:
        items = await paginate(
            conn,
            query=query,
            page=page,
            page_size=page_size,
        )

        return items

    @classmethod
    async def _get_total_items_count(cls, conn, query: Query) -> int:
        q = query.with_only_columns([func.count()]).order_by(None)

        cursor = await conn.execute(q)
        total = await cursor.scalar()

        return total

    @classmethod
    def filters(cls, table, query: Query, **params) -> Query:
        # filter_field = getattr(cls, cls.filter_field, None) \
        #     if cls.filter_field is not None \
        #     else getattr(cls, 'name', None)
        #
        # if filter_field is not None:
        #     if cls.desc:
        #         query = query.order_by(filter_field.desc())
        #     else:
        #         query = query.order_by(filter_field)

        for key, value in params.items():
            is_not_valid_filter = (
                not hasattr(table, key) or
                value is None
            )

            if is_not_valid_filter:
                continue

            field = getattr(table.columns, key, None)

            if isinstance(value, str):
                query = query.where(field.ilike('%{}%'.format(value)))
            elif isinstance(value, UUID):
                query = query.where(field == str(value))
            elif isinstance(value, Enum):
                query = query.where(field == value.name)
            else:
                query = query.where(field == value)

        return query

    @classmethod
    def revoke_filters(
            cls,
            table,
            query: Query,
            **params
    ) -> Query:
        for key, value in params.items():
            is_not_valid_filter = (
                not hasattr(table, key) or
                value is None
            )

            if is_not_valid_filter:
                continue

            field = getattr(table.columns, key, None)

            query = query.where(field != value)

        return query

    @classmethod
    async def get_by_filters(
            cls,
            conn,
            table,
            query: Query,
            page: int = 1,
            page_size: int = DEFAULT_PAGE_SIZE,
            rev_filters=None,
            **params: dict
    ) -> Pagination:
        if rev_filters is None:
            rev_filters = {}

        filters_ = cls.filters(table, query, **params)

        query = cls.revoke_filters(
            table,
            query=filters_,
            **rev_filters
        )

        items = await cls._get_paginated_items(conn, query, page, page_size)

        total = await cls._get_total_items_count(conn, query)

        return Pagination(items, total, page, page_size)

    # def getattr_from_column_name(self, name, default=Ellipsis):
    #     for attr, column in inspect(self.__class__).c.items():
    #         if column.name == name:
    #             return getattr(self, attr)
    #
    #     if default is Ellipsis:
    #         raise KeyError
    #     else:
    #         return default

    # @classmethod
    # def is_exists(cls, model_id: int = None, **fields) -> bool:
    #     pass

    # @classmethod
    # def exists_or_not_found(cls, model_id: int = None, **fields) -> None:
    #     if cls.is_exists(model_id, **fields):
    #         return
    #
    #     raise NoResultFound({'id': ['No row was found by id %d' % model_id]})

# def base_model() -> Type[Model]:
#     return Model
