from marshmallow import Schema, fields


class BasePaginationSchema(Schema):
    page = fields.Integer()
    page_size = fields.Integer(default=20, missing=20)
