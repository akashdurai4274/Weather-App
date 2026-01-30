from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.exceptions import ConflictError, NotFoundError
from app.schemas.watchlist import AddWatchlistRequest, WatchlistResponse
from app.services.watchlist_service import WatchlistService


def _make_mock_location(city="London", country="GB"):
    loc = MagicMock()
    loc.id = "loc-1"
    loc.city_name = city
    loc.country_code = country
    loc.latitude = 51.5
    loc.longitude = -0.1
    return loc


def _make_mock_watchlist_item(loc=None):
    item = MagicMock()
    item.id = "item-1"
    item.location = loc or _make_mock_location()
    item.added_at = MagicMock()
    item.added_at.isoformat.return_value = "2025-01-15T10:00:00+00:00"
    return item


@pytest.mark.asyncio
class TestWatchlistService:
    @patch("app.services.watchlist_service.WatchlistRepository")
    @patch("app.services.watchlist_service.LocationRepository")
    async def test_get_watchlist(self, mock_loc_repo_cls, mock_wl_repo_cls):
        mock_wl_repo = mock_wl_repo_cls.return_value
        mock_wl_repo.get_user_watchlist = AsyncMock(
            return_value=[_make_mock_watchlist_item()]
        )

        db = AsyncMock()
        service = WatchlistService(db)
        result = await service.get_watchlist("user-1")

        assert isinstance(result, WatchlistResponse)
        assert result.count == 1
        assert result.items[0].location.city_name == "London"

    @patch("app.services.watchlist_service.WatchlistRepository")
    @patch("app.services.watchlist_service.LocationRepository")
    async def test_add_location(self, mock_loc_repo_cls, mock_wl_repo_cls):
        mock_loc_repo = mock_loc_repo_cls.return_value
        mock_wl_repo = mock_wl_repo_cls.return_value

        loc = _make_mock_location()
        mock_loc_repo.get_or_create = AsyncMock(return_value=loc)
        mock_wl_repo.exists = AsyncMock(return_value=False)
        mock_wl_repo.add_item = AsyncMock(return_value=_make_mock_watchlist_item(loc))

        db = AsyncMock()
        service = WatchlistService(db)
        request = AddWatchlistRequest(city_name="London", country_code="GB")
        result = await service.add_location("user-1", request)

        assert result.location.city_name == "London"

    @patch("app.services.watchlist_service.WatchlistRepository")
    @patch("app.services.watchlist_service.LocationRepository")
    async def test_add_duplicate_location_raises_conflict(self, mock_loc_repo_cls, mock_wl_repo_cls):
        mock_loc_repo = mock_loc_repo_cls.return_value
        mock_wl_repo = mock_wl_repo_cls.return_value

        mock_loc_repo.get_or_create = AsyncMock(return_value=_make_mock_location())
        mock_wl_repo.exists = AsyncMock(return_value=True)

        db = AsyncMock()
        service = WatchlistService(db)
        request = AddWatchlistRequest(city_name="London")
        with pytest.raises(ConflictError):
            await service.add_location("user-1", request)

    @patch("app.services.watchlist_service.WatchlistRepository")
    @patch("app.services.watchlist_service.LocationRepository")
    async def test_remove_nonexistent_raises_not_found(self, mock_loc_repo_cls, mock_wl_repo_cls):
        mock_wl_repo = mock_wl_repo_cls.return_value
        mock_wl_repo.remove_item = AsyncMock(return_value=False)

        db = AsyncMock()
        service = WatchlistService(db)
        with pytest.raises(NotFoundError):
            await service.remove_location("user-1", "nonexistent")
