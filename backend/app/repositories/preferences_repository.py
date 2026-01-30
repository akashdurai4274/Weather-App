from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.preferences import UserPreferences


class PreferencesRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_user_id(self, user_id: str) -> UserPreferences | None:
        stmt = select(UserPreferences).where(UserPreferences.user_id == user_id)
        result = await self._db.execute(stmt)
        return result.scalars().first()

    async def create(self, prefs: UserPreferences) -> UserPreferences:
        self._db.add(prefs)
        await self._db.flush()
        return prefs

    async def upsert(self, user_id: str, **kwargs) -> UserPreferences:
        existing = await self.get_by_user_id(user_id)
        if existing:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(existing, key, value)
            await self._db.flush()
            return existing
        prefs = UserPreferences(user_id=user_id, **{k: v for k, v in kwargs.items() if v is not None})
        return await self.create(prefs)
