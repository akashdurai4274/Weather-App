
from unittest.mock import AsyncMock, patch 

import pytest

from app.schemas.weather import CurrentWeatherResponse, ForecastResponse
from app.services.weather_service import WeatherService
from app.core.exceptions import NotFoundError


MOCK_CURRENT_RESPONSE = {
    "data": [{
        "city_name": "London",
        "country_code": "GB",
        "temp": 15.5,
        "app_temp": 14.0,
        "rh": 72,
        "wind_spd": 5.2,
        "wind_cdir_full": "North-northwest",
        "weather": {"description": "Overcast clouds", "icon": "c04d"},
        "vis": 10,
        "pres": 1013,
        "uv": 3.5,
        "clouds": 90,
        "sunrise": "06:45",
        "sunset": "18:30",
        "aqi": 45,
        "lat": 51.5074,
        "lon": -0.1278,
    }]
}

MOCK_DAILY_RESPONSE = {
    "city_name": "London",
    "country_code": "GB",
    "lat": 51.5074,
    "lon": -0.1278,
    "data": [{
        "valid_date": "2025-01-15",
        "high_temp": 12,
        "low_temp": 5,
        "rh": 75,
        "wind_spd": 4.1,
        "weather": {"description": "Cloudy", "icon": "c03d"},
        "pop": 30,
    }],
}

MOCK_HOURLY_RESPONSE = {
    "data": [{
        "timestamp_local": "2025-01-15T10:00:00",
        "temp": 10.5,
        "app_temp": 9.0,
        "rh": 68,
        "wind_spd": 3.5,
        "weather": {"description": "Few clouds", "icon": "c02d"},
        "pop": 10,
    }],
}

MOCK_ALERTS_RESPONSE = {"alerts": []}


@pytest.mark.asyncio
class TestWeatherService:

    @patch("app.services.weather_service.weather_client")
    async def test_get_current_weather(self, mock_client):
        mock_client.get_current_weather = AsyncMock(
            return_value=(MOCK_CURRENT_RESPONSE, True)
        )

        service = WeatherService()
        result = await service.get_current(city="London")

        assert isinstance(result, CurrentWeatherResponse)
        assert result.data.city_name == "London"
        assert result.data.temp == 15.5
        assert result.data.description == "Overcast clouds"

        mock_client.get_current_weather.assert_called_once_with(
            city="London", lat=None, lon=None
        )

    @patch("app.services.weather_service.weather_client")
    async def test_get_current_weather_empty_data(self, mock_client):
        mock_client.get_current_weather = AsyncMock(
            return_value=({"data": []}, True)
        )

        service = WeatherService()

        with pytest.raises(NotFoundError):
            await service.get_current(city="NonexistentCity")

    @patch("app.services.weather_service.weather_client")
    async def test_get_forecast(self, mock_client):
        mock_client.get_forecast_daily = AsyncMock(
            return_value=(MOCK_DAILY_RESPONSE, True)
        )
        mock_client.get_forecast_hourly = AsyncMock(
            return_value=(MOCK_HOURLY_RESPONSE, True)
        )
        mock_client.get_alerts = AsyncMock(
            return_value=(MOCK_ALERTS_RESPONSE, True)
        )

        service = WeatherService()
        result = await service.get_forecast(city="London")

        assert isinstance(result, ForecastResponse)
        assert result.city_name == "London"
        assert len(result.daily) == 1
        assert len(result.hourly) == 1
        assert result.daily[0].date == "2025-01-15"
        assert result.hourly[0].temp == 10.5

    @patch("app.services.weather_service.weather_client")
    async def test_get_current_by_coordinates(self, mock_client):
        mock_client.get_current_weather = AsyncMock(
            return_value=(MOCK_CURRENT_RESPONSE, True)
        )

        service = WeatherService()
        result = await service.get_current(lat=51.5074, lon=-0.1278)

        assert result.data.city_name == "London"

        mock_client.get_current_weather.assert_called_once_with(
            city=None, lat=51.5074, lon=-0.1278
        )
