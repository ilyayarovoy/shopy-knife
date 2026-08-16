import pytest


@pytest.mark.asyncio
async def test_checkout_success(client, test_user, test_product):
    # Add item to cart
    await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })

    # Checkout
    response = await client.post(f"/api/orders/user/{test_user.id}/checkout")
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == test_user.id
    assert data["total_price"] == 199.98  # 99.99 * 2
    assert data["status"] == "new"
    assert data["id"] is not None

    # Verify cart is empty after checkout
    cart_response = await client.get(f"/api/cart/user/{test_user.id}")
    cart_data = cart_response.json()
    assert cart_data["total_items"] == 0
    assert len(cart_data["items"]) == 0


@pytest.mark.asyncio
async def test_checkout_empty_cart(client, test_user):
    response = await client.post(f"/api/orders/user/{test_user.id}/checkout")
    assert response.status_code == 400
    assert "Cart is empty" in response.json()["detail"]


@pytest.mark.asyncio
async def test_checkout_insufficient_stock(client, test_user, test_product):
    # Try to add more than available stock
    response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 100
    })
    # This should fail at cart level, but if stock changes, checkout should catch it
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_user_orders(client, test_user, test_product):
    # Create an order
    await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })
    await client.post(f"/api/orders/user/{test_user.id}/checkout")

    # Get orders
    response = await client.get(f"/api/orders/user/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["status"] == "new"


@pytest.mark.asyncio
async def test_get_user_orders_empty(client, test_user):
    response = await client.get(f"/api/orders/user/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 0
    assert len(data["items"]) == 0


@pytest.mark.asyncio
async def test_get_order_by_id(client, test_user, test_product):
    # Create an order
    add_response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })
    checkout_response = await client.post(f"/api/orders/user/{test_user.id}/checkout")
    order_id = checkout_response.json()["id"]

    # Get order
    response = await client.get(f"/api/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_get_order_by_id_not_found(client):
    response = await client.get(f"/api/orders/999")
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_order_status(client, test_user, test_product):
    # Create an order
    await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })
    checkout_response = await client.post(f"/api/orders/user/{test_user.id}/checkout")
    order_id = checkout_response.json()["id"]

    # Update status
    response = await client.put(f"/api/orders/{order_id}/user/{test_user.id}/status", json={
        "status": "processing"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processing"


@pytest.mark.asyncio
async def test_update_order_status_wrong_user(client, test_user, test_product):
    # Create an order for test_user
    await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })
    checkout_response = await client.post(f"/api/orders/user/{test_user.id}/checkout")
    order_id = checkout_response.json()["id"]

    # Try to update as different user
    response = await client.put(f"/api/orders/{order_id}/user/999/status", json={
        "status": "processing"
    })
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]


@pytest.mark.asyncio
async def test_checkout_updates_product_stock(client, test_user, test_product):
    # Get initial stock
    initial_stock = test_product.stock

    # Add to cart and checkout
    await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 3
    })
    await client.post(f"/api/orders/user/{test_user.id}/checkout")

    # Verify stock was decreased
    product_response = await client.get(f"/api/products/{test_product.id}")
    updated_product = product_response.json()
    assert updated_product["stock"] == initial_stock - 3
