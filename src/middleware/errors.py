from aiohttp.web import middleware, HTTPException
from lib.errors.base import (
    no_result_found_handler,
    validation_error_handler,
)
import marshmallow


@middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except HTTPException as ex:
        if ex.status_code == 404:
            return no_result_found_handler(ex)
        raise
    except marshmallow.exceptions.ValidationError as ex:
        return validation_error_handler(ex)
