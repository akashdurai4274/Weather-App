import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestWatchlistAPI:
    async def test_get_empty_watchlist(self, client: AsyncClient, auth_headers):
        response = await client.get("/api/v1/watchlist", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["items"] == []

    async def test_add_to_watchlist(self, client: AsyncClient, auth_headers):
        response = await client.post(
            "/api/v1/watchlist",
            headers=auth_headers,
            json={"city_name": "Paris", "country_code": "FR"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["location"]["city_name"] == "Paris"

    async def test_add_duplicate_to_watchlist(self, client: AsyncClient, auth_headers):
        await client.post(
            "/api/v1/watchlist",
            headers=auth_headers,
            json={"city_name": "Berlin", "country_code": "DE"},
        )
        response = await client.post(
            "/api/v1/watchlist",
            headers=auth_headers,
            json={"city_name": "Berlin", "country_code": "DE"},
        )
        assert response.status_code == 409

    async def test_remove_from_watchlist(self, client: AsyncClient, auth_headers):
        add_resp = await client.post(
            "/api/v1/watchlist",
            headers=auth_headers,
            json={"city_name": "Tokyo", "country_code": "JP"},
        )
        item_id = add_resp.json()["id"]
        response = await client.delete(
            f"/api/v1/watchlist/{item_id}", headers=auth_headers
        )
        assert response.status_code == 204

    async def test_remove_nonexistent_item(self, client: AsyncClient, auth_headers):
        response = await client.delete(
            "/api/v1/watchlist/nonexistent-id", headers=auth_headers
        )
        assert response.status_code == 404

    async def test_watchlist_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/v1/watchlist")
        assert response.status_code == 403
