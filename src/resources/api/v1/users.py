from aiohttp import web
from src.models.user import User
from src.schemas.user import (
    UserSchema,
    UsersFilterSchema,
)
from sqlalchemy import select
import lib.sqlalchemy as salib
import json


class UsersCollectionController(web.View):
    async def get(self):
        data = UsersFilterSchema().load(self.request.query)
        async with self.request.app['db'].acquire() as conn:
            query = select([User]).where(
                User.deleted.is_(False)
            )
            pagination = User.get_by_filters(conn, query=query, **data)

        items = UserSchema(many=True).dump(await pagination.items)
        return web.json_response(
            text=json.dumps(
                await salib.with_pagination_meta(items, pagination)
            )
        )
