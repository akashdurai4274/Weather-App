import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictError, ForbiddenError, InvalidCredentialsError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import SignupRequest, TokenResponse, UserResponse

logger = structlog.get_logger()


class AuthService:
    def __init__(self, db: AsyncSession):
        self._repo = UserRepository(db)

    async def signup(self, data: SignupRequest) -> UserResponse:
        if await self._repo.exists_by_username(data.username):
            raise ConflictError(detail=f"Username '{data.username}' is already taken")

        user = User(
            username=data.username,
            hashed_password=hash_password(data.password),
        )
        
        print(user)
        created = await self._repo.create(user)
        logger.info("user_created", username=created.username, user_id=created.id)
        return UserResponse.model_validate(created)

    async def login(self, username: str, password: str) -> TokenResponse:
        user = await self._repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError(detail="Invalid username or password")
        if not user.is_active:
            raise InvalidCredentialsError(detail="Account is disabled")

        access_token = create_access_token(
            subject=user.id, extra_claims={"role": user.role}
        )
        refresh_token = create_refresh_token(subject=user.id)
        logger.info("user_logged_in", user_id=user.id)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            role=user.role,
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise InvalidCredentialsError(detail="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise InvalidCredentialsError(detail="Invalid token")

        user = await self._repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise InvalidCredentialsError(detail="User not found or disabled")

        new_access = create_access_token(
            subject=user.id, extra_claims={"role": user.role}
        )
        new_refresh = create_refresh_token(subject=user.id)
        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            user_id=user.id,
            role=user.role,
        )

    async def promote_to_admin(self, user_id: str, secret_key: str) -> UserResponse:
        if secret_key != settings.ADMIN_SECRET_KEY:
            raise ForbiddenError(detail="Invalid admin secret key")

        user = await self._repo.update_role(user_id, "ADMIN")
        if not user:
            raise InvalidCredentialsError(detail="User not found")

        logger.info("user_promoted_to_admin", user_id=user.id)
        return UserResponse.model_validate(user)
