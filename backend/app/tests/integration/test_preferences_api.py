import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestPreferencesAPI:
    async def test_get_default_preferences(self, client: AsyncClient, auth_headers):
        response = await client.get("/api/v1/preferences", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["units"] == "metric"
        assert data["default_city"] is None

    async def test_update_preferences(self, client: AsyncClient, auth_headers):
        response = await client.put(
            "/api/v1/preferences",
            headers=auth_headers,
            json={"default_city": "New York", "units": "imperial"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["default_city"] == "New York"
        assert data["units"] == "imperial"

    async def test_get_updated_preferences(self, client: AsyncClient, auth_headers):
        await client.put(
            "/api/v1/preferences",
            headers=auth_headers,
            json={"default_city": "Sydney", "default_country": "AU"},
        )
        response = await client.get("/api/v1/preferences", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["default_city"] == "Sydney"

    async def test_preferences_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/v1/preferences")
        assert response.status_code == 403
