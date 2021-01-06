from models.user import User
from sqlalchemy import select
from lib.sqlalchemy import Pagination


class UsersBLOC:

    @classmethod
    async def get_paginated_users(
            cls, conn,
            with_deleted: bool = False, **filters: dict,
    ) -> Pagination:
        query = select([User])

        if not with_deleted:
            query = query.where(
                User.deleted.is_(False)
            )

        pagination = await User.get_by_filters(conn, query, **filters)

        return pagination
