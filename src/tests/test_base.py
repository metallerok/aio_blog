import pytest
from logging import getLogger

logger = getLogger("aio_blog.tests")


async def test_1(client, create_tables):
    print("Default test", flush=True)

    response = await client.get("/api/v1/api_info")
    body = await response.get_data()
    print(body, flush=True)
