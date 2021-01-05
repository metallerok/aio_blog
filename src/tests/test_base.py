from logging import getLogger

logger = getLogger("aio_blog.tests")


async def test_api_info(client):

    response = await client.get("/api/v1/api_info")

    assert response.status == 200

    body = await response.json()

    assert body == {'status': 'ok', 'result': 'success'}
