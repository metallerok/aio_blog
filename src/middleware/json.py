import json
from aiohttp.web import middleware, HTTPUnprocessableEntity
from json.decoder import JSONDecodeError


@middleware
async def json_handler(request, handler):
    if request.content_type == "application/json":
        try:
            body = await request.json()
            request["json"] = body
        except JSONDecodeError:
            raise HTTPUnprocessableEntity(
                text=json.dumps({
                    "error_message": "Invalid json"
                })
            )
    else:
        request["json"] = {}

    resp = await handler(request)

    return resp
