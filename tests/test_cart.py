import pytest


@pytest.mark.asyncio
async def test_add_to_cart(client, test_user, test_product):
    response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 2
    assert data["product_id"] == test_product.id
    assert data["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_add_to_cart_product_not_found(client, test_user):
    response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": 999,
        "quantity": 1
    })
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_to_cart_insufficient_stock(client, test_user, test_product):
    response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 100
    })
    assert response.status_code == 400
    assert "Not enough stock" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_user_cart(client, test_user, test_product):
    # Add item to cart
    await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })

    # Get cart
    response = await client.get(f"/api/cart/user/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 2
    assert data["total_price"] == 199.98  # 99.99 * 2
    assert len(data["items"]) == 1


@pytest.mark.asyncio
async def test_update_cart_item(client, test_user, test_product):
    # Add item to cart
    add_response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })
    item_id = add_response.json()["id"]

    # Update quantity
    response = await client.put(f"/api/cart/item/{item_id}", json={
        "quantity": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 5


@pytest.mark.asyncio
async def test_update_cart_item_insufficient_stock(client, test_user, test_product):
    # Add item to cart
    add_response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })
    item_id = add_response.json()["id"]

    # Try to update quantity beyond stock
    response = await client.put(f"/api/cart/item/{item_id}", json={
        "quantity": 100
    })
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_remove_from_cart(client, test_user, test_product):
    # Add item to cart
    add_response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })
    item_id = add_response.json()["id"]

    # Remove from cart
    response = await client.delete(f"/api/cart/item/{item_id}")
    assert response.status_code == 200

    # Verify removal
    cart_response = await client.get(f"/api/cart/user/{test_user.id}")
    cart_data = cart_response.json()
    assert cart_data["total_items"] == 0


@pytest.mark.asyncio
async def test_clear_user_cart(client, test_user, test_product):
    # Add multiple items
    await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })

    # Clear cart
    response = await client.delete(f"/api/cart/user/{test_user.id}/clear")
    assert response.status_code == 200

    # Verify empty cart
    cart_response = await client.get(f"/api/cart/user/{test_user.id}")
    cart_data = cart_response.json()
    assert cart_data["total_items"] == 0
    assert len(cart_data["items"]) == 0


@pytest.mark.asyncio
async def test_increment_existing_cart_item(client, test_user, test_product):
    # Add item first time
    await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 2
    })

    # Add same item again
    response = await client.post(f"/api/cart/user/{test_user.id}/add", json={
        "product_id": test_product.id,
        "quantity": 3
    })

    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 5  # 2 + 3
