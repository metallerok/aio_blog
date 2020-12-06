from aiohttp import web
from typing import Optional
from functools import partial, wraps
from lib.decorators import resource

from lib import BASE_URL_PREFIX_V1

routes = web.RouteTableDef()

api_resource = partial(
    resource,
    prefix=BASE_URL_PREFIX_V1,
    router=routes
)


def url(url_: Optional[str] = None) -> str:
    if url_ is None:
        return BASE_URL_PREFIX_V1
    else:
        return "%s/%s" % (BASE_URL_PREFIX_V1, url_)
