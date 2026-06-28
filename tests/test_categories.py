import pytest


@pytest.mark.asyncio
async def test_create_category(client):
    response = await client.post("/api/categories", json={
        "name": "Chef Knives",
        "slug": "chef-knives",
        "description": "Professional chef knives"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Chef Knives"
    assert data["slug"] == "chef-knives"


@pytest.mark.asyncio
async def test_get_all_categories(client, test_category):
    response = await client.get("/api/categories/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Kitchen Knives"


@pytest.mark.asyncio
async def test_get_category_by_id(client, test_category):
    response = await client.get(f"/api/categories/{test_category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_category.id
    assert data["name"] == "Kitchen Knives"


@pytest.mark.asyncio
async def test_get_category_not_found(client):
    response = await client.get("/api/categories/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_category(client, test_category):
    response = await client.put(f"/api/categories/{test_category.id}", json={
        "name": "Updated Kitchen Knives",
        "slug": "updated-kitchen-knives"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Kitchen Knives"


@pytest.mark.asyncio
async def test_delete_category(client, test_category):
    response = await client.delete(f"/api/categories/{test_category.id}")
    assert response.status_code == 200

    # Verify deletion
    check_response = await client.get(f"/api/categories/{test_category.id}")
    assert check_response.status_code == 404
