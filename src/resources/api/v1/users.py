import logging
from psycopg2 import errors as db_errors
from aiohttp import web
from src.schemas.user import (
    UserSchema,
    UsersFilterSchema,
    UserInsertSchema,
)
from blocs.users import UsersBLOC
from resources.api.v1 import api_resource

import lib.sqlalchemy as salib
import json

logger = logging.getLogger("m_blog_users_service")


@api_resource("/users")
class UsersCollectionController(web.View):
    async def get(self):
        """ returns paginated users list """
        filters = UsersFilterSchema().load(self.request.query)

        async with self.request.app['db'].acquire() as conn:
            pagination = await UsersBLOC.get_paginated(conn, **filters)

        items = UserSchema(many=True).dump(pagination.items)
        result = salib.with_pagination_meta(items, pagination)

        return web.json_response(text=json.dumps(result))

    async def post(self):
        """ create user """
        data = UserInsertSchema().load(self.request["json"])

        async with self.request.app['db'].acquire() as conn:
            try:
                res = await UsersBLOC.insert(conn, data)
            except db_errors.UniqueViolation as e:
                logger.exception(e)
                raise web.HTTPBadRequest(
                    content_type="application/json",
                    text=json.dumps({
                        "error_message": "User already exists",
                        "error_code": 1001,
                    })
                )

        return web.json_response(
            text=json.dumps(UserSchema().dump(res))
        )
