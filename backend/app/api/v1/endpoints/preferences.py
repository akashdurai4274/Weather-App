from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user_id
from app.db.session import get_db
from app.schemas.preferences import PreferencesResponse, UpdatePreferencesRequest
from app.services.preferences_service import PreferencesService

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.get("", response_model=PreferencesResponse)
async def get_preferences(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = PreferencesService(db)
    return await service.get_preferences(user_id)


@router.put("", response_model=PreferencesResponse)
async def update_preferences(
    data: UpdatePreferencesRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = PreferencesService(db)
    return await service.update_preferences(user_id, data)
