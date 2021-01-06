from aiohttp import web
from src.schemas.user import (
    UserSchema,
    UsersFilterSchema,
    UserInsertSchema,
)
from blocs.users import UsersBLOC
from resources.api.v1 import api_resource
from models.user import User
import lib.sqlalchemy as salib
import json
from sqlalchemy import insert, literal_column


@api_resource("/users")
class UsersCollectionController(web.View):
    async def get(self):
        filters = UsersFilterSchema().load(self.request.query)

        async with self.request.app['db'].acquire() as conn:
            pagination = await UsersBLOC.get_paginated_users(conn, **filters)

        items = UserSchema(many=True).dump(pagination.items)
        result = salib.with_pagination_meta(items, pagination)

        return web.json_response(text=json.dumps(result))

    async def post(self):
        data = UserInsertSchema().load(self.request["json"])

        async with self.request.app['db'].acquire() as conn:
            password = User.make_password_hash(data.pop("password"))
            qr = insert(User).values(
                phone=data["phone"],
                email=data["email"],
                type=data["type"],
                login=data["login"],
                password=password,
                name=data["name"],
                surname=data["surname"],
                middle_name=data["middle_name"],
            ).returning(literal_column('*'))
            cursor = await conn.execute(qr)

            res = await cursor.fetchone()
            print(res)

        return web.json_response(
            text=json.dumps(UserSchema().dump(res))
        )
