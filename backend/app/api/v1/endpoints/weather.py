from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user_id
from app.schemas.weather import CurrentWeatherResponse, ForecastResponse
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    city: str | None = Query(None, min_length=1, max_length=100),
    lat: float | None = Query(None, ge=-90, le=90),
    lon: float | None = Query(None, ge=-180, le=180),
    _user_id: str = Depends(get_current_user_id),
):
    service = WeatherService()
    return await service.get_current(city=city, lat=lat, lon=lon)


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    city: str | None = Query(None, min_length=1, max_length=100),
    lat: float | None = Query(None, ge=-90, le=90),
    lon: float | None = Query(None, ge=-180, le=180),
    _user_id: str = Depends(get_current_user_id),
):
    service = WeatherService()
    return await service.get_forecast(city=city, lat=lat, lon=lon)
