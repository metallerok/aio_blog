from aiohttp.web import RouteTableDef


def resource(resource_uri: str, router: RouteTableDef, prefix: str = '', ):
    def wrapper(cls):
        url = prefix + resource_uri
        router.view(url)(cls)
    return wrapper
