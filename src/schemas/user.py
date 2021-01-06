from marshmallow import Schema, fields
from app_types.users import UserType
# from lib.errors.base import HTTPUnprocessableEntity
from src.schemas.base import BasePaginationSchema


class UserSchema(Schema):
    uuid = fields.UUID()

    login = fields.String(allow_none=True)
    password = fields.String(load_only=True, required=False)

    name = fields.String(allow_none=True)
    surname = fields.String(allow_none=True)
    middle_name = fields.String(allow_none=True)

    phone = fields.String(allow_none=True)
    email = fields.Email(allow_none=True)

    type = fields.Method(
        serialize="serialize_type",
        deserialize="deserialize_type",
    )

    active = fields.Boolean()
    deleted = fields.Boolean()

    # access_level_id = fields.Integer()
    # access_level = fields.Nested(AccessLevelSchema)

    created = fields.DateTime()
    updated = fields.DateTime()

    @staticmethod
    def serialize_type(obj):
        return obj.type.name

    @staticmethod
    def deserialize_type(value):
        value = value.upper()
        if value in [t.name for t in UserType]:
            return UserType[value]
        else:
            raise Exception
            # raise HTTPUnprocessableEntity(
            #     description={
            #         "type": {
            #             "value": "unsupported value"
            #         },
            #     }
            # )


class UsersFilterSchema(BasePaginationSchema):
    uuid = fields.UUID()

    login = fields.String(allow_none=True)

    name = fields.String(allow_none=True)
    surname = fields.String(allow_none=True)
    middle_name = fields.String(allow_none=True)

    phone = fields.String(allow_none=True)
    email = fields.Email(allow_none=True)

    type = fields.Method(
        deserialize="deserialize_type",
    )

    active = fields.Boolean()
    deleted = fields.Boolean()

    # access_level_id = fields.Integer()

    created = fields.Date()
    updated = fields.Date()

    @staticmethod
    def deserialize_type(value):
        value = value.upper()
        if value in [t.name for t in UserType]:
            return UserType[value]
        else:
            # raise HTTPUnprocessableEntity(
            #     description={
            #         "type": {
            #             "value": "unsupported value"
            #         },
            #     }
            # )
            raise Exception
