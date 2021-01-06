from aiohttp import web
from src.schemas.user import (
    UserSchema,
    UsersFilterSchema,
)
from blocs.users import UsersBLOC
from resources.api.v1 import api_resource
import lib.sqlalchemy as salib
import json


@api_resource("/users")
class UsersCollectionController(web.View):
    async def get(self):
        filters = UsersFilterSchema().load(self.request.query)

        async with self.request.app['db'].acquire() as conn:
            pagination = await UsersBLOC.get_paginated_users(conn, **filters)

        items = UserSchema(many=True).dump(pagination.items)
        result = salib.with_pagination_meta(items, pagination)

        return web.json_response(text=json.dumps(result))
