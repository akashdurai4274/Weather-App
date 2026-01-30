import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.watchlist import WatchlistItem
from app.repositories.location_repository import LocationRepository
from app.repositories.watchlist_repository import WatchlistRepository
from app.schemas.watchlist import (
    AddWatchlistRequest,
    WatchlistItemResponse,
    WatchlistLocationResponse,
    WatchlistResponse,
)

logger = structlog.get_logger()


class WatchlistService:
    def __init__(self, db: AsyncSession):
        self._watchlist_repo = WatchlistRepository(db)
        self._location_repo = LocationRepository(db)

    async def get_watchlist(self, user_id: str) -> WatchlistResponse:
        items = await self._watchlist_repo.get_user_watchlist(user_id)
        response_items = []
        for item in items:
            loc = item.location
            response_items.append(WatchlistItemResponse(
                id=item.id,
                location=WatchlistLocationResponse(
                    id=loc.id,
                    city_name=loc.city_name,
                    country_code=loc.country_code,
                    latitude=loc.latitude,
                    longitude=loc.longitude,
                ),
                added_at=item.added_at.isoformat(),
            ))
        return WatchlistResponse(items=response_items, count=len(response_items))

    async def add_location(self, user_id: str, data: AddWatchlistRequest) -> WatchlistItemResponse:
        location = await self._location_repo.get_or_create(
            city_name=data.city_name,
            country_code=data.country_code,
            latitude=data.latitude,
            longitude=data.longitude,
        )

        if await self._watchlist_repo.exists(user_id, location.id):
            raise ConflictError(detail=f"'{data.city_name}' is already in your watchlist")

        item = WatchlistItem(user_id=user_id, location_id=location.id)
        created = await self._watchlist_repo.add_item(item)
        loc = created.location
        logger.info("watchlist_item_added", user_id=user_id, city=data.city_name)
        return WatchlistItemResponse(
            id=created.id,
            location=WatchlistLocationResponse(
                id=loc.id,
                city_name=loc.city_name,
                country_code=loc.country_code,
                latitude=loc.latitude,
                longitude=loc.longitude,
            ),
            added_at=created.added_at.isoformat(),
        )

    async def remove_location(self, user_id: str, item_id: str) -> None:
        removed = await self._watchlist_repo.remove_item(item_id, user_id)
        if not removed:
            raise NotFoundError(detail="Watchlist item not found")
        logger.info("watchlist_item_removed", user_id=user_id, item_id=item_id)
