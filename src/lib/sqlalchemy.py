from typing import Type
from sqlalchemy import func

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



