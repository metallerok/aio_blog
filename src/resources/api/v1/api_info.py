from aiohttp import web
import json
from resources.api.v1 import api_resource


@api_resource("/api_info")
class ApiInfoController(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            cursor = await conn.execute("select 'success';")
            result = await cursor.fetchone()

        return web.json_response(
            text=json.dumps({
                "status": "ok",
                "result": result[0]
            })
        )
