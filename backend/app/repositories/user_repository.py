from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_id(self, user_id: str) -> User | None:
        stmt = (
            select(User)
            .options(joinedload(User.preferences))
            .where(User.id == user_id)
        )
        result = await self._db.execute(stmt)
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self._db.execute(stmt)
        return result.scalars().first()

    async def create(self, user: User) -> User:
        self._db.add(user)
        await self._db.flush()
        return user

    async def exists_by_username(self, username: str) -> bool:
        stmt = select(User.id).where(User.username == username)
        result = await self._db.execute(stmt)
        return result.scalars().first() is not None

    async def update_role(self, user_id: str, role: str) -> User | None:
        user = await self.get_by_id(user_id)
        if user:
            user.role = role
            await self._db.flush()
        return user
