from aiohttp import web
import json


class ApiInfoController(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            cursor = await conn.execute("select 'success';")
            result = await cursor.fetchone()
        return web.Response(
            text=json.dumps({
                "status": "ok",
                "result": result[0]
            })
        )
