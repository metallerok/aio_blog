import json
from marshmallow import Schema, fields, validate
from aiohttp.web import HTTPUnprocessableEntity
from app_types.users import UserType
from src.schemas.base import BasePaginationSchema

phone_validator = validate.Regexp(
    "^((7)+([0-9]){10})$", 0,
    'Invalid phone format'
)


def _deserialize_user_type(value):
    value = value.upper()
    if value in [t.name for t in UserType]:
        return UserType[value]
    else:
        raise HTTPUnprocessableEntity(
            text=json.dumps({
                "type": ["Unsupported value"],
            })
        )


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
        return _deserialize_user_type(value)


class UserInsertSchema(Schema):
    login = fields.String(required=True)
    password = fields.String(required=True)

    phone = fields.String(required=False, default=None, missing=None, validate=phone_validator)
    email = fields.Email(required=False, default=None, missing=None)

    name = fields.String(required=False)
    surname = fields.String(required=False)
    middle_name = fields.String(required=False)

    type = fields.Method(
        serialize="serialize_type",
        deserialize="deserialize_type",
    )

    @staticmethod
    def deserialize_type(value):
        return _deserialize_user_type(value)


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
        return _deserialize_user_type(value)
