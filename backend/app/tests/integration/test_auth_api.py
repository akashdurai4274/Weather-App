import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthAPI:
    async def test_signup_success(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/signup",
            json={"username": "newuser", "password": "Password123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["role"] == "USER"
        assert "id" in data

    async def test_signup_duplicate_username(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/signup",
            json={"username": "dupeuser", "password": "Password123"},
        )
        response = await client.post(
            "/api/v1/auth/signup",
            json={"username": "dupeuser", "password": "Password456"},
        )
        assert response.status_code == 409

    async def test_signup_invalid_username(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/signup",
            json={"username": "ab", "password": "Password123"},
        )
        assert response.status_code == 422

    async def test_signup_short_password(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/signup",
            json={"username": "validuser", "password": "short"},
        )
        assert response.status_code == 422

    async def test_login_success(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/signup",
            json={"username": "loginuser", "password": "Password123"},
        )
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "loginuser", "password": "Password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/signup",
            json={"username": "loginuser2", "password": "Password123"},
        )
        response = await client.post(
            "/api/v1/auth/login",
            json={"username": "loginuser2", "password": "WrongPassword"},
        )
        assert response.status_code == 401

    async def test_refresh_token(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/signup",
            json={"username": "refreshuser", "password": "Password123"},
        )
        login_resp = await client.post(
            "/api/v1/auth/login",
            json={"username": "refreshuser", "password": "Password123"},
        )
        refresh_token = login_resp.json()["refresh_token"]

        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    async def test_get_me_authenticated(self, client: AsyncClient, auth_headers):
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"

    async def test_get_me_unauthenticated(self, client: AsyncClient):
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 403
