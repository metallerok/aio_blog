from typing import Type
from sqlalchemy import func
from sqlalchemy.orm import Query
from uuid import UUID
from enum import Enum

from math import ceil

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import inspect

DEFAULT_PAGE_SIZE = 20


async def paginate(conn, query, page, page_size):
    selectable = query.limit(page_size).offset(
        (page - 1) * page_size
    )
    cursor = await conn.execute(selectable)
    return await cursor.fetchall()


class AsyncPagination:
    __slots__ = ['conn', 'query', 'page', 'page_size']

    def __init__(self, conn, query, page: int, page_size: int):
        self.conn = conn
        self.query = query
        self.page = page
        self.page_size = page_size

    @property
    async def items(self) -> list:
        return await paginate(
            self.conn,
            self.query,
            self.page,
            self.page_size
        )

    @property
    async def total_pages(self) -> int:
        total = await self.total
        return ceil(total / self.page_size) or 1

    @property
    async def total(self) -> int:
        q = self.query.with_only_columns([func.count()]).order_by(None)
        cursor = await self.conn.execute(q)
        total = await cursor.scalar()
        return total


async def with_pagination_meta(models: list, pagination: AsyncPagination):
    page = pagination.page
    total_pages = await pagination.total_pages
    page_size = pagination.page_size
    return {
        'data': models,
        'meta': {
            'current_page': page,
            'total_pages': total_pages,
            'page_size': page_size
        }
    }


class Model:

    filter_field = None
    desc = False

    @classmethod
    def filters(cls, query: Query, **params) -> Query:
        filter_field = getattr(cls, cls.filter_field, None) \
            if cls.filter_field is not None \
            else getattr(cls, 'name', None)

        if filter_field is not None:
            if cls.desc:
                query = query.order_by(filter_field.desc())
            else:
                query = query.order_by(filter_field)

        for key, value in params.items():
            is_not_valid_filter = (
                    not hasattr(cls, key) or
                    value is None
            )

            if is_not_valid_filter:
                continue

            field = getattr(cls, key, None)

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
            query: Query,
            **params
    ) -> Query:
        for key, value in params.items():
            is_not_valid_filter = (
                    not hasattr(cls, key) or
                    value is None
            )

            if is_not_valid_filter:
                continue

            field = getattr(cls, key, None)

            query = query.where(field != value)

        return query

    @classmethod
    def get_by_filters(
            cls,
            conn,
            query: Query,
            page: int = 1,
            page_size: int = DEFAULT_PAGE_SIZE,
            rev_filters=None,
            **params: dict
    ) -> AsyncPagination:
        if rev_filters is None:
            rev_filters = {}
        filters_ = cls.filters(query, **params)
        return AsyncPagination(
            conn,
            query=cls.revoke_filters(
                query=filters_,
                **rev_filters
            ),
            page=page,
            page_size=page_size
        )

    def to_dict(self):
        return dict((prop.key, getattr(self, prop.key))
                    for prop in inspect(self).mapper.iterate_properties)

    def getattr_from_column_name(self, name, default=Ellipsis):
        for attr, column in inspect(self.__class__).c.items():
            if column.name == name:
                return getattr(self, attr)

        if default is Ellipsis:
            raise KeyError
        else:
            return default

    @classmethod
    def is_exists(cls, model_id: int = None, **fields) -> bool:
        pass

    @classmethod
    def exists_or_not_found(cls, model_id: int = None, **fields) -> None:
        if cls.is_exists(model_id, **fields):
            return

        raise NoResultFound({'id': ['No row was found by id %d' % model_id]})

    def __str__(self):
        return str(self.to_dict())


def base_model() -> Type[Model]:
    return Model



