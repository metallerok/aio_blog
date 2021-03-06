import bcrypt
from aiopg.sa.result import RowProxy
from models.user import user
from sqlalchemy import select, literal_column
from lib.sqlalchemy import Pagination, SaQuery


class UsersBLOC:

    @staticmethod
    def make_password_hash(password):
        hash_ = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())

        return hash_.decode('utf-8')

    @staticmethod
    def is_password_valid(password, password_hash):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @classmethod
    async def get_paginated(
            cls, conn,
            with_deleted: bool = False, **filters: dict,
    ) -> Pagination:

        login = filters.pop("login", None)
        email = filters.pop("email", None)

        query = select([user])

        if not with_deleted:
            query = query.where(
                user.c.deleted.is_(False)
            )

        if login:
            query = query.where(
                user.c.login == login
            )

        if email:
            query = query.where(
                user.c.email == email
            )

        pagination = await SaQuery.get_by_filters(conn, user, query, **filters)

        return pagination

    @classmethod
    async def insert(cls, conn, data: dict) -> RowProxy:
        password = UsersBLOC.make_password_hash(data.pop("password"))

        qr = user.insert().values(
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

        return res

    @classmethod
    async def get_by_uuid(cls, conn,  uuid: str, delted: bool = False):
        query = select([user]).where(user.c.uuid == uuid)

        if delted:
            query = query.where(user.c.deleted is True)

        cursor = await conn.execute(query)

        res = await cursor.fetchone()

        return res
