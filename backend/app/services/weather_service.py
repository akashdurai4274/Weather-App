"""Weather service - transforms raw API data into application DTOs."""

import asyncio

import structlog

from app.schemas.weather import (
    CurrentWeatherData,
    CurrentWeatherResponse,
    DailyForecast,
    ForecastResponse,
    HourlyForecast,
    WeatherAlert,
)
from app.services.weather_client import weather_client

logger = structlog.get_logger()


class WeatherService:
    async def get_current(
        self, city: str | None = None, lat: float | None = None, lon: float | None = None
    ) -> CurrentWeatherResponse:
        raw, is_mock = await weather_client.get_current_weather(city=city, lat=lat, lon=lon)
        data_list = raw.get("data", [])
        if not data_list:
            from app.core.exceptions import NotFoundError
            raise NotFoundError(detail="No weather data found for the given location")

        d = data_list[0]
        weather_data = CurrentWeatherData(
            city_name=d.get("city_name", ""),
            country_code=d.get("country_code", ""),
            temp=d.get("temp", 0),
            feels_like=d.get("app_temp", 0),
            humidity=d.get("rh", 0),
            wind_speed=d.get("wind_spd", 0),
            wind_direction=d.get("wind_cdir_full", ""),
            description=d.get("weather", {}).get("description", ""),
            icon=d.get("weather", {}).get("icon", ""),
            visibility=d.get("vis"),
            pressure=d.get("pres"),
            uv_index=d.get("uv"),
            clouds=d.get("clouds"),
            sunrise=d.get("sunrise"),
            sunset=d.get("sunset"),
            aqi=d.get("aqi"),
            lat=d.get("lat", 0),
            lon=d.get("lon", 0),
        )
        return CurrentWeatherResponse(
            data=weather_data,
            data_source="mock" if is_mock else "live",
        )

    async def get_forecast(
        self, city: str | None = None, lat: float | None = None, lon: float | None = None
    ) -> ForecastResponse:
        (daily_raw, daily_mock), (hourly_raw, hourly_mock) = await asyncio.gather(
            weather_client.get_forecast_daily(city=city, lat=lat, lon=lon, days=5),
            weather_client.get_forecast_hourly(city=city, lat=lat, lon=lon, hours=48),
        )

        daily_list = []
        for d in daily_raw.get("data", []):
            daily_list.append(DailyForecast(
                date=d.get("valid_date", ""),
                temp_high=d.get("high_temp", d.get("max_temp", 0)),
                temp_low=d.get("low_temp", d.get("min_temp", 0)),
                humidity=d.get("rh"),
                wind_speed=d.get("wind_spd"),
                description=d.get("weather", {}).get("description", ""),
                icon=d.get("weather", {}).get("icon", ""),
                pop=d.get("pop"),
            ))

        hourly_list = []
        for h in hourly_raw.get("data", []):
            hourly_list.append(HourlyForecast(
                timestamp=h.get("timestamp_local", h.get("datetime", "")),
                temp=h.get("temp", 0),
                feels_like=h.get("app_temp"),
                humidity=h.get("rh"),
                wind_speed=h.get("wind_spd"),
                description=h.get("weather", {}).get("description", ""),
                icon=h.get("weather", {}).get("icon", ""),
                pop=h.get("pop"),
            ))

        city_name = daily_raw.get("city_name", "")
        country_code = daily_raw.get("country_code", "")
        lat_val = daily_raw.get("lat", 0)
        lon_val = daily_raw.get("lon", 0)

        # Fetch alerts if we have coordinates
        alerts_list: list[WeatherAlert] = []
        alerts_mock = False
        if lat_val and lon_val:
            alerts_raw, alerts_mock = await weather_client.get_alerts(lat=lat_val, lon=lon_val)
            for a in alerts_raw.get("alerts", []):
                alerts_list.append(WeatherAlert(
                    title=a.get("title", ""),
                    description=a.get("description", ""),
                    severity=a.get("severity"),
                    expires=a.get("expires_local"),
                    regions=a.get("regions", []),
                ))

        is_mock = daily_mock or hourly_mock or alerts_mock

        return ForecastResponse(
            city_name=city_name,
            country_code=country_code,
            lat=lat_val,
            lon=lon_val,
            daily=daily_list,
            hourly=hourly_list,
            alerts=alerts_list,
            data_source="mock" if is_mock else "live",
        )
