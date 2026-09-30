from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_item(client: TestClient, user_token_headers: dict):
    """
    Test creating an item associated with the current user.
    """
    payload = {
        "title": "Test Item",
        "description": "A description for the test item",
    }
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=user_token_headers,
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert "id" in data
    assert "owner_id" in data


def test_read_items(client: TestClient, user_token_headers: dict):
    """
    Test retrieving items list for current user.
    """
    client.post(
        f"{settings.API_V1_STR}/items/",
        headers=user_token_headers,
        json={"title": "Item 1", "description": "First item"},
    )
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=user_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read_item_by_id(client: TestClient, user_token_headers: dict):
    """
    Test reading a single item by id.
    """
    create_res = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=user_token_headers,
        json={"title": "Single Item", "description": "Details here"},
    )
    item_id = create_res.json()["id"]

    response = client.get(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers=user_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == item_id


def test_update_item(client: TestClient, user_token_headers: dict):
    """
    Test updating an item's details.
    """
    create_res = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=user_token_headers,
        json={"title": "Old Title", "description": "Old Description"},
    )
    item_id = create_res.json()["id"]

    update_payload = {"title": "Updated Title"}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers=user_token_headers,
        json=update_payload,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Title"
    assert response.json()["description"] == "Old Description"


def test_delete_item(client: TestClient, user_token_headers: dict):
    """
    Test deleting an item.
    """
    create_res = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=user_token_headers,
        json={"title": "To Delete", "description": "Will be removed"},
    )
    item_id = create_res.json()["id"]

    delete_res = client.delete(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers=user_token_headers,
    )
    assert delete_res.status_code == status.HTTP_200_OK

    get_res = client.get(
        f"{settings.API_V1_STR}/items/{item_id}",
        headers=user_token_headers,
    )
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_items_access(client: TestClient):
    """
    Test that accessing items endpoints without token returns 401.
    """
    response = client.get(f"{settings.API_V1_STR}/items/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
