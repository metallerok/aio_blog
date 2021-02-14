from resources.api.v1 import url
import copy

base_insert_user_data = {
    "phone": "invalid phone",
    "email": "invalid email",
    "type": "ADMIN",
    "login": "test",
    "password": "masterkey",
    "name": "test2 name",
    "surname": "test2 surname",
    "middle_name": "test2 middlename"
}


async def test_create_user_with_invalid_params(client):
    url_ = url("/users")

    data = copy.copy(base_insert_user_data)
    resp = await client.post(url_, json=data)

    assert resp.status == 422

    resp_body = await resp.json()

    assert "email" in resp_body
    assert "phone" in resp_body


async def test_create_user(client):
    url_ = url("/users")

    data = copy.copy(base_insert_user_data)
    data["phone"] = "79991112233"
    data["email"] = "test@mail.com"

    resp = await client.post(url_, json=data)

    assert resp.status == 200

    resp_body = await resp.json()

    assert "password" in resp_body
    assert data["phone"] == resp_body["phone"]
    assert data["email"] == resp_body["email"]
    assert data["type"] == resp_body["type"]
    assert data["login"] == resp_body["login"]
    assert data["name"] == resp_body["name"]
    assert data["surname"] == resp_body["surname"]
    assert data["middle_name"] == resp_body["middle_name"]
