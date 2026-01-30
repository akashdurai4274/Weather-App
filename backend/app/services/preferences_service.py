from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.preferences_repository import PreferencesRepository
from app.schemas.preferences import PreferencesResponse, UpdatePreferencesRequest


class PreferencesService:
    def __init__(self, db: AsyncSession):
        self._repo = PreferencesRepository(db)

    async def get_preferences(self, user_id: str) -> PreferencesResponse:
        prefs = await self._repo.get_by_user_id(user_id)
        if not prefs:
            return PreferencesResponse(
                default_city=None,
                default_country=None,
                default_lat=None,
                default_lon=None,
                units="metric",
            )
        return PreferencesResponse.model_validate(prefs)

    async def update_preferences(self, user_id: str, data: UpdatePreferencesRequest) -> PreferencesResponse:
        update_data = data.model_dump(exclude_none=True)
        prefs = await self._repo.upsert(user_id, **update_data)
        return PreferencesResponse.model_validate(prefs)
