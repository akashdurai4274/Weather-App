"""Centralized WeatherBit API client with retry, timeout, TTL cache, rate-limiting and graceful degradation."""

import time
import asyncio
import structlog
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.core.config import settings
from app.core.exceptions import ExternalAPIError, RateLimitError

logger = structlog.get_logger()

CACHE_TTL_SECONDS = 300  # 5 minutes — matches frontend staleTime and mock bucket
MIN_REQUEST_INTERVAL = 0.5  # seconds between external API calls


class WeatherBitClient:
    """HTTP client for WeatherBit API via RapidAPI with TTL cache and global rate-limiter."""

    def __init__(self):
        self._base_url = settings.WEATHERBIT_BASE_URL
        self._headers = {
            "x-rapidapi-key": settings.RAPIDAPI_KEY,
            "x-rapidapi-host": settings.RAPIDAPI_HOST,
        }
        self._timeout = httpx.Timeout(settings.API_TIMEOUT_SECONDS)
        self._cache: dict[str, tuple[float, dict]] = {}
        self._cache_locks: dict[str, asyncio.Lock] = {}
        self._rate_lock = asyncio.Lock()
        self._last_request_time = 0.0

    def _build_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            headers=self._headers,
            timeout=self._timeout,
        )

    def _cache_key(self, endpoint: str, params: dict) -> str:
        sorted_params = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        return f"{endpoint}?{sorted_params}"

    def _get_cached(self, key: str) -> dict | None:
        entry = self._cache.get(key)
        if entry is None:
            return None
        cached_at, data = entry
        if time.monotonic() - cached_at > CACHE_TTL_SECONDS:
            del self._cache[key]
            return None
        return data

    def _set_cached(self, key: str, data: dict) -> None:
        self._cache[key] = (time.monotonic(), data)

    def _get_cache_lock(self, key: str) -> asyncio.Lock:
        if key not in self._cache_locks:
            self._cache_locks[key] = asyncio.Lock()
        return self._cache_locks[key]

    async def _rate_limited_fetch(self, url: str, params: dict) -> httpx.Response:
        """Make an HTTP request while respecting the global rate limit."""
        async with self._rate_lock:
            now = time.monotonic()
            wait = MIN_REQUEST_INTERVAL - (now - self._last_request_time)
            if wait > 0:
                await asyncio.sleep(wait)
            async with self._build_client() as client:
                response = await client.get(url, params=params)
            self._last_request_time = time.monotonic()
            return response

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=3),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True,
    )
    async def _request(self, endpoint: str, params: dict) -> dict:
        key = self._cache_key(endpoint, params)

        # Fast path: return cached data without locking
        cached = self._get_cached(key)
        if cached is not None:
            logger.info("weather_api_cache_hit", endpoint=endpoint)
            return cached

        # Serialize requests for the same cache key to avoid duplicate API calls
        lock = self._get_cache_lock(key)
        async with lock:
            cached = self._get_cached(key)
            if cached is not None:
                logger.info("weather_api_cache_hit", endpoint=endpoint)
                return cached

            url = f"{self._base_url}{endpoint}"
            logger.info("weather_api_request", endpoint=endpoint, params=params)
            response = await self._rate_limited_fetch(url, params)

            if response.status_code == 429:
                raise RateLimitError()
            if response.status_code >= 500:
                raise ExternalAPIError(detail=f"WeatherBit API error: {response.status_code}")
            if response.status_code >= 400:
                raise ExternalAPIError(
                    detail=f"WeatherBit API client error: {response.status_code} - {response.text}"
                )

            data = response.json()
            self._set_cached(key, data)
            return data

    async def get_current_weather(
        self, city: str | None = None, lat: float | None = None, lon: float | None = None
    ) -> tuple[dict, bool]:
        from app.services.geocoding import validate_city, reverse_geocode

        params: dict = {}
        geo_info = None

        if city:
            # Validate city via geocoding
            geo_info = await validate_city(city)
            if geo_info:
                params["lat"] = str(geo_info["lat"])
                params["lon"] = str(geo_info["lon"])
            else:
                params["city"] = city
        elif lat is not None and lon is not None:
            params["lat"] = str(lat)
            params["lon"] = str(lon)
            geo_info = await reverse_geocode(lat, lon)
        else:
            params["city"] = settings.DEFAULT_CITY

        try:
            data = await self._request("/current", params)
            # Enhance with geocoded info if available
            if geo_info and data.get("data"):
                data["data"][0]["city_name"] = geo_info.get("city", data["data"][0].get("city_name", ""))
                data["data"][0]["country_code"] = geo_info.get("country", data["data"][0].get("country_code", ""))
            return data, False
        except (ExternalAPIError, RateLimitError, httpx.TimeoutException, httpx.ConnectError) as e:
            logger.warning("weather_api_fallback_mock", endpoint="/current", error=str(e))
            from app.services.mock_weather import generate_current_async
            return await generate_current_async(city=city, lat=lat, lon=lon), True

    async def get_forecast_daily(
        self, city: str | None = None, lat: float | None = None, lon: float | None = None, days: int = 5
    ) -> tuple[dict, bool]:
        from app.services.geocoding import validate_city, reverse_geocode

        params: dict = {"days": str(days)}
        geo_info = None

        if city:
            geo_info = await validate_city(city)
            if geo_info:
                params["lat"] = str(geo_info["lat"])
                params["lon"] = str(geo_info["lon"])
            else:
                params["city"] = city
        elif lat is not None and lon is not None:
            params["lat"] = str(lat)
            params["lon"] = str(lon)
            geo_info = await reverse_geocode(lat, lon)
        else:
            params["city"] = settings.DEFAULT_CITY

        try:
            data = await self._request("/forecast/daily", params)
            if geo_info:
                data["city_name"] = geo_info.get("city", data.get("city_name", ""))
                data["country_code"] = geo_info.get("country", data.get("country_code", ""))
            return data, False
        except (ExternalAPIError, RateLimitError, httpx.TimeoutException, httpx.ConnectError) as e:
            logger.warning("weather_api_fallback_mock", endpoint="/forecast/daily", error=str(e))
            from app.services.mock_weather import generate_forecast_daily_async
            return await generate_forecast_daily_async(city=city, lat=lat, lon=lon, days=days), True

    async def get_forecast_hourly(
        self, city: str | None = None, lat: float | None = None, lon: float | None = None, hours: int = 48
    ) -> tuple[dict, bool]:
        from app.services.geocoding import validate_city, reverse_geocode

        params: dict = {"hours": str(hours)}
        geo_info = None

        if city:
            geo_info = await validate_city(city)
            if geo_info:
                params["lat"] = str(geo_info["lat"])
                params["lon"] = str(geo_info["lon"])
            else:
                params["city"] = city
        elif lat is not None and lon is not None:
            params["lat"] = str(lat)
            params["lon"] = str(lon)
            geo_info = await reverse_geocode(lat, lon)
        else:
            params["city"] = settings.DEFAULT_CITY

        try:
            data = await self._request("/forecast/hourly", params)
            if geo_info:
                data["city_name"] = geo_info.get("city", data.get("city_name", ""))
                data["country_code"] = geo_info.get("country", data.get("country_code", ""))
            return data, False
        except (ExternalAPIError, RateLimitError, httpx.TimeoutException, httpx.ConnectError) as e:
            logger.warning("weather_api_fallback_mock", endpoint="/forecast/hourly", error=str(e))
            from app.services.mock_weather import generate_forecast_hourly_async
            return await generate_forecast_hourly_async(city=city, lat=lat, lon=lon, hours=hours), True

    async def get_alerts(self, lat: float, lon: float) -> tuple[dict, bool]:
        params = {"lat": str(lat), "lon": str(lon)}
        try:
            data = await self._request("/alerts", params)
            return data, False
        except (ExternalAPIError, RateLimitError, httpx.TimeoutException, httpx.ConnectError) as e:
            logger.warning("weather_alerts_fallback_mock", error=str(e))
            from app.services.mock_weather import generate_alerts
            return generate_alerts(), True


weather_client = WeatherBitClient()
