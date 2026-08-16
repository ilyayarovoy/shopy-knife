import pytest


@pytest.mark.asyncio
async def test_add_to_favorites(client, test_user, test_product):
    response = await client.post(f"/api/favorites/user/{test_user.id}/add", json={
        "product_id": test_product.id
    })
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == test_product.id
    assert data["user_id"] == test_user.id


@pytest.mark.asyncio
async def test_add_to_favorites_product_not_found(client, test_user):
    response = await client.post(f"/api/favorites/user/{test_user.id}/add", json={
        "product_id": 999
    })
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_duplicate_to_favorites(client, test_user, test_product):
    # Add to favorites first time
    await client.post(f"/api/favorites/user/{test_user.id}/add", json={
        "product_id": test_product.id
    })

    # Add same item again
    response = await client.post(f"/api/favorites/user/{test_user.id}/add", json={
        "product_id": test_product.id
    })

    # Should return existing item without error (due to unique constraint handling)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == test_product.id


@pytest.mark.asyncio
async def test_get_user_favorites(client, test_user, test_product):
    # Add item to favorites
    await client.post(f"/api/favorites/user/{test_user.id}/add", json={
        "product_id": test_product.id
    })

    # Get favorites
    response = await client.get(f"/api/favorites/user/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product.id


@pytest.mark.asyncio
async def test_get_user_favorites_empty(client, test_user):
    response = await client.get(f"/api/favorites/user/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 0
    assert len(data["items"]) == 0


@pytest.mark.asyncio
async def test_remove_from_favorites(client, test_user, test_product):
    # Add item to favorites
    add_response = await client.post(f"/api/favorites/user/{test_user.id}/add", json={
        "product_id": test_product.id
    })
    item_id = add_response.json()["id"]

    # Remove from favorites
    response = await client.delete(f"/api/favorites/user/{test_user.id}/item/{item_id}")
    assert response.status_code == 204

    # Verify removal
    get_response = await client.get(f"/api/favorites/user/{test_user.id}")
    data = get_response.json()
    assert data["total_count"] == 0


@pytest.mark.asyncio
async def test_remove_from_favorites_item_not_found(client, test_user):
    response = await client.delete(f"/api/favorites/user/{test_user.id}/item/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_is_product_favorite(client, test_user, test_product):
    # Check before adding
    response = await client.get(f"/api/favorites/user/{test_user.id}/check/{test_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_favorite"] is False

    # Add to favorites
    await client.post(f"/api/favorites/user/{test_user.id}/add", json={
        "product_id": test_product.id
    })

    # Check after adding
    response = await client.get(f"/api/favorites/user/{test_user.id}/check/{test_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_favorite"] is True


@pytest.mark.asyncio
async def test_is_product_favorite_not_added(client, test_user, test_product):
    response = await client.get(f"/api/favorites/user/{test_user.id}/check/{test_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_favorite"] is False


@pytest.mark.asyncio
async def test_remove_favorite_wrong_user(client, test_user, test_product):
    # Add item to favorites for test_user
    add_response = await client.post(f"/api/favorites/user/{test_user.id}/add", json={
        "product_id": test_product.id
    })
    item_id = add_response.json()["id"]

    # Try to remove with different user_id
    response = await client.delete(f"/api/favorites/user/999/item/{item_id}")
    assert response.status_code == 403
