from fastapi import APIRouter

from app.api.v1.endpoints import auth, preferences, watchlist, weather

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(weather.router)
api_router.include_router(watchlist.router)
api_router.include_router(preferences.router)
