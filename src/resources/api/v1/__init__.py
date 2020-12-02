from typing import Optional
from functools import partial

from lib import BASE_URL_PREFIX_V1
from lib.decorators import resource

api_resource = partial(resource, prefix=BASE_URL_PREFIX_V1)


def url(url_: Optional[str] = None) -> str:
    if url_ is None:
        return BASE_URL_PREFIX_V1
    else:
        return "%s/%s" % (BASE_URL_PREFIX_V1, url_)
