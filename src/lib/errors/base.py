import json
from aiohttp import web


def validation_error_handler(ex):
    raise web.HTTPUnprocessableEntity(
        text=json.dumps(ex.messages),
        content_type="application/json",
    )


def no_result_found_handler(ex):
    raise web.HTTPNotFound(
        content_type="application/json"
    )
