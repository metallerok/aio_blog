from aiohttp import web
from src.models.user import User
from src.schemas.user import UserSchema
from sqlalchemy import select
from src.lib.sqlalchemy import AsyncPagination, with_pagination_meta
import json


class UsersCollectionController(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            query = select([User]).where(
                User.deleted.is_(False)
            )

            pagination = AsyncPagination(conn, query, page=1, page_size=1)

        items = UserSchema(many=True).dump(await pagination.items)

        return web.Response(
            text=json.dumps(
                await with_pagination_meta(items, pagination)
            )
        )
