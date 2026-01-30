import pytest

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_password_returns_hash(self):
        hashed = hash_password("mypassword")
        assert hashed != "mypassword"
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        hashed = hash_password("mypassword")
        assert verify_password("mypassword", hashed) is True

    def test_verify_password_incorrect(self):
        hashed = hash_password("mypassword")
        assert verify_password("wrongpassword", hashed) is False


class TestJWT:
    def test_create_access_token(self):
        token = create_access_token(subject="user123")
        payload = decode_token(token)
        assert payload["sub"] == "user123"
        assert payload["type"] == "access"

    def test_create_refresh_token(self):
        token = create_refresh_token(subject="user123")
        payload = decode_token(token)
        assert payload["sub"] == "user123"
        assert payload["type"] == "refresh"

    def test_access_token_extra_claims(self):
        token = create_access_token(subject="user123", extra_claims={"role": "USER"})
        payload = decode_token(token)
        assert payload["role"] == "USER"

    def test_decode_invalid_token(self):
        from app.core.exceptions import InvalidCredentialsError
        with pytest.raises(InvalidCredentialsError):
            decode_token("invalid.token.here")
