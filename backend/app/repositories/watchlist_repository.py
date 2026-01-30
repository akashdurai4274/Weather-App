from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.watchlist import WatchlistItem


class WatchlistRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_user_watchlist(self, user_id: str) -> list[WatchlistItem]:
        stmt = (
            select(WatchlistItem)
            .options(joinedload(WatchlistItem.location))
            .where(WatchlistItem.user_id == user_id)
            .order_by(WatchlistItem.added_at.desc())
        )
        result = await self._db.execute(stmt)
        return list(result.scalars().unique().all())

    async def add_item(self, item: WatchlistItem) -> WatchlistItem:
        self._db.add(item)
        await self._db.flush()
        # Reload with location joined
        stmt = (
            select(WatchlistItem)
            .options(joinedload(WatchlistItem.location))
            .where(WatchlistItem.id == item.id)
        )
        result = await self._db.execute(stmt)
        return result.scalars().first()  # type: ignore

    async def remove_item(self, item_id: str, user_id: str) -> bool:
        stmt = (
            delete(WatchlistItem)
            .where(WatchlistItem.id == item_id, WatchlistItem.user_id == user_id)
        )
        result = await self._db.execute(stmt)
        return result.rowcount > 0  # type: ignore

    async def exists(self, user_id: str, location_id: str) -> bool:
        stmt = select(WatchlistItem.id).where(
            WatchlistItem.user_id == user_id,
            WatchlistItem.location_id == location_id,
        )
        result = await self._db.execute(stmt)
        return result.scalars().first() is not None
