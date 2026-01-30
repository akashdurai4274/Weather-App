from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidCredentialsError
from app.core.security import decode_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository

security_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> str:
    payload = decode_token(credentials.credentials)
    if payload.get("type") != "access":
        raise InvalidCredentialsError(detail="Invalid token type")
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise InvalidCredentialsError(detail="Token missing subject")
    return user_id


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise InvalidCredentialsError(detail="User not found")
    return user
