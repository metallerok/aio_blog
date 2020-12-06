from aiohttp.web import middleware


@middleware
async def logging(request, handler):
    resp = await handler(request)
    return resp
