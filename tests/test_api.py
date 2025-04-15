import pytest


@pytest.mark.asyncio
async def test_회원가입(client):
    data = {
        "email": "test-user@test.com",
        "password": "password",
        "password_check": "password",
    }
    response = await client.post("/auth/register", json=data)
    assert response.status_code == 200
    return response.json()


@pytest.mark.asyncio
async def test_회원가입_비밀번호_불일치(client):
    data = {
        "email": "test-user@test.com",
        "password": "password",
        "password_check": "1234",
    }
    response = await client.post("/auth/register", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_로그인(client):
    await test_회원가입(client)

    data = {"email": "test-user@test.com", "password": "password"}
    response = await client.post("/auth/login", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_로그인_실패(client):
    await test_회원가입(client)

    data = {"email": "test-user@test.com", "password": "1234"}
    response = await client.post("/auth/login", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_상품_리스트_조회(client, create_products):
    response = await client.get("/products")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_상품_조회(client, create_products):
    product_id = create_products[0]

    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 200
    product = response.json()
    assert len(product["items"]) == 4
    return product


@pytest.mark.asyncio
async def test_존재하지_않는_상품_조회(client, create_products):
    product_id = create_products[0]

    response = await client.get(f"/products/{product_id + 999}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_주문_요청(client, create_products):
    product = await test_상품_조회(client, create_products)
    auth = await test_회원가입(client)
    client.headers = {"Authorization": f"JWT {auth["token"]}"}

    data = {
        "order_number": "test",
        "product_id": product["id"],
        "items": [
            {"item_id": product["items"][0]["id"], "quantity": 3},
            {"item_id": product["items"][1]["id"], "quantity": 2},
        ],
    }
    response = await client.post("/orders", json=data)
    assert response.status_code == 200
    order = response.json()
    assert len(order["items"]) == 5
    return order


@pytest.mark.asyncio
async def test_재고_없이_주문시_실패(client, create_products):
    product = await test_상품_조회(client, create_products)
    auth = await test_회원가입(client)
    client.headers = {"Authorization": f"JWT {auth["token"]}"}

    data = {
        "order_number": "test",
        "product_id": product["id"],
        "items": [
            {"item_id": product["items"][0]["id"], "quantity": 0},
            {"item_id": product["items"][1]["id"], "quantity": 2},
        ],
    }
    response = await client.post("/orders", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_품목_없이_주문시_실패(client, create_products):
    product = await test_상품_조회(client, create_products)
    auth = await test_회원가입(client)
    client.headers = {"Authorization": f"JWT {auth["token"]}"}

    data = {"order_number": "test", "product_id": product["id"], "items": []}
    response = await client.post("/orders", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_동일한_주문번호로_주문시_실패(client, create_products):
    product = await test_주문_요청(client, create_products)

    data = {
        "order_number": "test",
        "product_id": product["id"],
        "items": [
            {"item_id": product["items"][0]["id"], "quantity": 1},
            {"item_id": product["items"][1]["id"], "quantity": 1},
        ],
    }
    response = await client.post("/orders",  json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_주문_조회(client, create_products):
    order = await test_주문_요청(client, create_products)

    response = await client.get(f"/orders/{order["id"]}")
    assert response.status_code == 200
    order = response.json()
    assert len(order["items"]) == 5
