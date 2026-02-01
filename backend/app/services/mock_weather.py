"""Dynamic mock weather data generator — produces realistic, time-varying data
that mimics the WeatherBit API raw response format."""

import hashlib
import math
import time
from datetime import datetime, timedelta, timezone

CITY_DB: dict[str, dict] = {
    "london": {"lat": 51.51, "lon": -0.13, "cc": "GB"},
    "new york": {"lat": 40.71, "lon": -74.01, "cc": "US"},
    "tokyo": {"lat": 35.68, "lon": 139.69, "cc": "JP"},
    "paris": {"lat": 48.86, "lon": 2.35, "cc": "FR"},
    "sydney": {"lat": -33.87, "lon": 151.21, "cc": "AU"},
    "mumbai": {"lat": 19.08, "lon": 72.88, "cc": "IN"},
    "chennai": {"lat": 13.08, "lon": 80.27, "cc": "IN"},
    "delhi": {"lat": 28.61, "lon": 77.21, "cc": "IN"},
    "new delhi": {"lat": 28.61, "lon": 77.21, "cc": "IN"},
    "bangalore": {"lat": 12.97, "lon": 77.59, "cc": "IN"},
    "bengaluru": {"lat": 12.97, "lon": 77.59, "cc": "IN"},
    "hyderabad": {"lat": 17.39, "lon": 78.49, "cc": "IN"},
    "kolkata": {"lat": 22.57, "lon": 88.36, "cc": "IN"},
    "pune": {"lat": 18.52, "lon": 73.86, "cc": "IN"},
    "ahmedabad": {"lat": 23.02, "lon": 72.57, "cc": "IN"},
    "jaipur": {"lat": 26.91, "lon": 75.79, "cc": "IN"},
    "lucknow": {"lat": 26.85, "lon": 80.95, "cc": "IN"},
    "kanpur": {"lat": 26.45, "lon": 80.35, "cc": "IN"},
    "nagpur": {"lat": 21.15, "lon": 79.09, "cc": "IN"},
    "indore": {"lat": 22.72, "lon": 75.86, "cc": "IN"},
    "thane": {"lat": 19.22, "lon": 72.98, "cc": "IN"},
    "bhopal": {"lat": 23.26, "lon": 77.41, "cc": "IN"},
    "visakhapatnam": {"lat": 17.69, "lon": 83.22, "cc": "IN"},
    "patna": {"lat": 25.59, "lon": 85.14, "cc": "IN"},
    "vadodara": {"lat": 22.31, "lon": 73.18, "cc": "IN"},
    "ghaziabad": {"lat": 28.67, "lon": 77.44, "cc": "IN"},
    "ludhiana": {"lat": 30.90, "lon": 75.86, "cc": "IN"},
    "coimbatore": {"lat": 11.01, "lon": 76.97, "cc": "IN"},
    "madurai": {"lat": 9.93, "lon": 78.12, "cc": "IN"},
    "kochi": {"lat": 9.93, "lon": 76.27, "cc": "IN"},
    "trivandrum": {"lat": 8.52, "lon": 76.94, "cc": "IN"},
    "thiruvananthapuram": {"lat": 8.52, "lon": 76.94, "cc": "IN"},
    "dubai": {"lat": 25.20, "lon": 55.27, "cc": "AE"},
    "singapore": {"lat": 1.35, "lon": 103.82, "cc": "SG"},
    "berlin": {"lat": 52.52, "lon": 13.41, "cc": "DE"},
    "moscow": {"lat": 55.76, "lon": 37.62, "cc": "RU"},
    "beijing": {"lat": 39.90, "lon": 116.40, "cc": "CN"},
    "cairo": {"lat": 30.04, "lon": 31.24, "cc": "EG"},
    "los angeles": {"lat": 34.05, "lon": -118.24, "cc": "US"},
    "toronto": {"lat": 43.65, "lon": -79.38, "cc": "CA"},
    "sao paulo": {"lat": -23.55, "lon": -46.63, "cc": "BR"},
    "nairobi": {"lat": -1.29, "lon": 36.82, "cc": "KE"},
    "seoul": {"lat": 37.57, "lon": 126.98, "cc": "KR"},
    "bangkok": {"lat": 13.76, "lon": 100.50, "cc": "TH"},
    "istanbul": {"lat": 41.01, "lon": 28.98, "cc": "TR"},
    "rome": {"lat": 41.90, "lon": 12.50, "cc": "IT"},
}

WEATHER_CONDITIONS = [
    {"description": "Clear Sky", "icon": "c01d"},
    {"description": "Few Clouds", "icon": "c02d"},
    {"description": "Scattered Clouds", "icon": "c02d"},
    {"description": "Broken Clouds", "icon": "c03d"},
    {"description": "Overcast Clouds", "icon": "c04d"},
    {"description": "Light Rain", "icon": "r01d"},
    {"description": "Moderate Rain", "icon": "r02d"},
    {"description": "Thunderstorm", "icon": "t01d"},
    {"description": "Mist", "icon": "a01d"},
    {"description": "Haze", "icon": "a05d"},
]

WIND_DIRS = [
    "North", "North-northeast", "Northeast", "East-northeast",
    "East", "East-southeast", "Southeast", "South-southeast",
    "South", "South-southwest", "Southwest", "West-southwest",
    "West", "West-northwest", "Northwest", "North-northwest",
]


def _hash_seed(key: str) -> float:
    """Return a deterministic float [0, 1) from a string key."""
    digest = hashlib.md5(key.encode()).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def _bucket() -> int:
    """5-minute bucket so data changes every 5 minutes."""
    return int(time.time()) // 300


_geo_cache: dict[str, tuple] = {}


async def _resolve_city_async(city: str | None, lat: float | None, lon: float | None):
    """Resolve inputs to (city_name, lat, lon, country_code) with geocoding fallback."""
    from app.services.geocoding import validate_city, reverse_geocode

    if city:
        key = city.lower().strip()
        if key in CITY_DB:
            info = CITY_DB[key]
            return city.title(), info["lat"], info["lon"], info["cc"]
        # Try geocoding API
        cache_key = f"city:{key}"
        if cache_key in _geo_cache:
            return _geo_cache[cache_key]
        geo = await validate_city(city)
        if geo:
            result = (geo["city"], geo["lat"], geo["lon"], geo["country"])
            _geo_cache[cache_key] = result
            return result
        return None  # Invalid city

    if lat is not None and lon is not None:
        # Check local DB first
        best_name, best_cc = None, None
        best_dist = float("inf")
        for name, info in CITY_DB.items():
            dist = (info["lat"] - lat) ** 2 + (info["lon"] - lon) ** 2
            if dist < best_dist:
                best_dist = dist
                best_name = name.title()
                best_cc = info["cc"]
        if best_dist < 1:  # Close enough
            return best_name, lat, lon, best_cc
        # Try reverse geocoding
        cache_key = f"coords:{lat:.2f},{lon:.2f}"
        if cache_key in _geo_cache:
            return _geo_cache[cache_key]
        geo = await reverse_geocode(lat, lon)
        if geo:
            result = (geo["city"], lat, lon, geo["country"])
            _geo_cache[cache_key] = result
            return result
        if best_name:
            return best_name, lat, lon, best_cc
        return "Unknown", lat, lon, "XX"

    return "London", 51.51, -0.13, "GB"


def _resolve_city(city: str | None, lat: float | None, lon: float | None):
    """Sync version - uses cache only, no API calls."""
    if city:
        key = city.lower().strip()
        if key in CITY_DB:
            info = CITY_DB[key]
            return city.title(), info["lat"], info["lon"], info["cc"]
        cache_key = f"city:{key}"
        if cache_key in _geo_cache:
            return _geo_cache[cache_key]
        h = _hash_seed(key)
        return city.title(), 20 + h * 40, -10 + h * 100, "XX"

    if lat is not None and lon is not None:
        cache_key = f"coords:{lat:.2f},{lon:.2f}"
        if cache_key in _geo_cache:
            return _geo_cache[cache_key]
        best_name, best_cc = "Unknown", "XX"
        best_dist = float("inf")
        for name, info in CITY_DB.items():
            dist = (info["lat"] - lat) ** 2 + (info["lon"] - lon) ** 2
            if dist < best_dist:
                best_dist = dist
                best_name = name.title()
                best_cc = info["cc"]
        if best_dist > 400:
            best_name, best_cc = "Local Area", "XX"
        return best_name, lat, lon, best_cc

    return "London", 51.51, -0.13, "GB"


def _base_temp(lat: float) -> float:
    """Latitude-based base temperature: equator ~30°C, poles ~-10°C."""
    abs_lat = abs(lat)
    return 30 - (abs_lat / 90) * 40


def _time_variation(hour: float) -> float:
    """Day/night cycle: warmest at 14:00, coolest at 05:00."""
    return 5 * math.sin((hour - 5) * math.pi / 12)


def _temp_now(lat: float, seed_key: str) -> float:
    now = datetime.now(timezone.utc)
    hour = now.hour + now.minute / 60
    base = _base_temp(lat)
    diurnal = _time_variation(hour)
    noise = (_hash_seed(f"{seed_key}:{_bucket()}") - 0.5) * 4
    return round(base + diurnal + noise, 1)


def _weather_index(seed_key: str) -> int:
    return int(_hash_seed(f"{seed_key}:wx:{_bucket()}") * len(WEATHER_CONDITIONS))


async def generate_current_async(
    city: str | None = None, lat: float | None = None, lon: float | None = None
) -> dict:
    result = await _resolve_city_async(city, lat, lon)
    if result is None:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(detail=f"City '{city}' not found")
    city_name, rlat, rlon, cc = result
    seed = f"{city_name}:{rlat:.2f}:{rlon:.2f}"
    temp = _temp_now(rlat, seed)
    wx = WEATHER_CONDITIONS[_weather_index(seed)]
    h = _hash_seed(f"{seed}:{_bucket()}")

    return {
        "data": [
            {
                "city_name": city_name,
                "country_code": cc,
                "temp": temp,
                "app_temp": round(temp - 1.5 + h * 2, 1),
                "rh": int(40 + h * 50),
                "wind_spd": round(1 + h * 10, 1),
                "wind_cdir_full": WIND_DIRS[int(h * len(WIND_DIRS))],
                "weather": wx,
                "vis": round(5 + h * 15, 1),
                "pres": round(1005 + h * 20, 1),
                "uv": round(1 + h * 10, 1),
                "clouds": int(h * 100),
                "sunrise": "06:15",
                "sunset": "18:30",
                "aqi": int(20 + h * 80),
                "lat": round(rlat, 4),
                "lon": round(rlon, 4),
            }
        ]
    }


def generate_current(
    city: str | None = None, lat: float | None = None, lon: float | None = None
) -> dict:
    city_name, rlat, rlon, cc = _resolve_city(city, lat, lon)
    seed = f"{city_name}:{rlat:.2f}:{rlon:.2f}"
    temp = _temp_now(rlat, seed)
    wx = WEATHER_CONDITIONS[_weather_index(seed)]
    h = _hash_seed(f"{seed}:{_bucket()}")

    return {
        "data": [
            {
                "city_name": city_name,
                "country_code": cc,
                "temp": temp,
                "app_temp": round(temp - 1.5 + h * 2, 1),
                "rh": int(40 + h * 50),
                "wind_spd": round(1 + h * 10, 1),
                "wind_cdir_full": WIND_DIRS[int(h * len(WIND_DIRS))],
                "weather": wx,
                "vis": round(5 + h * 15, 1),
                "pres": round(1005 + h * 20, 1),
                "uv": round(1 + h * 10, 1),
                "clouds": int(h * 100),
                "sunrise": "06:15",
                "sunset": "18:30",
                "aqi": int(20 + h * 80),
                "lat": round(rlat, 4),
                "lon": round(rlon, 4),
            }
        ]
    }


async def generate_forecast_daily_async(
    city: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    days: int = 5,
) -> dict:
    result = await _resolve_city_async(city, lat, lon)
    if result is None:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(detail=f"City '{city}' not found")
    city_name, rlat, rlon, cc = result
    return _generate_forecast_daily_data(city_name, rlat, rlon, cc, days)


def generate_forecast_daily(
    city: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    days: int = 5,
) -> dict:
    city_name, rlat, rlon, cc = _resolve_city(city, lat, lon)
    return _generate_forecast_daily_data(city_name, rlat, rlon, cc, days)


def _generate_forecast_daily_data(city_name: str, rlat: float, rlon: float, cc: str, days: int) -> dict:
    seed = f"{city_name}:{rlat:.2f}:{rlon:.2f}"
    base = _base_temp(rlat)
    today = datetime.now(timezone.utc).date()

    data = []
    for i in range(days):
        d = today + timedelta(days=i)
        day_seed = f"{seed}:d:{d.isoformat()}"
        h = _hash_seed(day_seed)
        high = round(base + 3 + h * 6, 1)
        low = round(base - 3 - h * 4, 1)
        wx = WEATHER_CONDITIONS[int(h * len(WEATHER_CONDITIONS))]
        data.append(
            {
                "valid_date": d.isoformat(),
                "high_temp": high,
                "low_temp": low,
                "rh": int(40 + h * 50),
                "wind_spd": round(1 + h * 10, 1),
                "weather": wx,
                "pop": int(h * 100),
            }
        )

    return {
        "city_name": city_name,
        "country_code": cc,
        "lat": round(rlat, 4),
        "lon": round(rlon, 4),
        "data": data,
    }


async def generate_forecast_hourly_async(
    city: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    hours: int = 48,
) -> dict:
    result = await _resolve_city_async(city, lat, lon)
    if result is None:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(detail=f"City '{city}' not found")
    city_name, rlat, rlon, cc = result
    return _generate_forecast_hourly_data(city_name, rlat, rlon, cc, hours)


def generate_forecast_hourly(
    city: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    hours: int = 48,
) -> dict:
    city_name, rlat, rlon, cc = _resolve_city(city, lat, lon)
    return _generate_forecast_hourly_data(city_name, rlat, rlon, cc, hours)


def _generate_forecast_hourly_data(city_name: str, rlat: float, rlon: float, cc: str, hours: int) -> dict:
    seed = f"{city_name}:{rlat:.2f}:{rlon:.2f}"
    base = _base_temp(rlat)
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

    data = []
    for i in range(hours):
        ts = now + timedelta(hours=i)
        hour_seed = f"{seed}:h:{ts.isoformat()}"
        h = _hash_seed(hour_seed)
        hour_f = ts.hour + ts.minute / 60
        temp = round(base + _time_variation(hour_f) + (h - 0.5) * 3, 1)
        wx = WEATHER_CONDITIONS[int(h * len(WEATHER_CONDITIONS))]
        data.append(
            {
                "timestamp_local": ts.strftime("%Y-%m-%dT%H:%M:%S"),
                "temp": temp,
                "app_temp": round(temp - 1 + h * 2, 1),
                "rh": int(40 + h * 50),
                "wind_spd": round(1 + h * 8, 1),
                "weather": wx,
                "pop": int(h * 80),
            }
        )

    return {
        "city_name": city_name,
        "country_code": cc,
        "lat": round(rlat, 4),
        "lon": round(rlon, 4),
        "data": data,
    }


def generate_alerts() -> dict:
    """Mock alerts — returns empty most of the time, occasional alert."""
    bucket = _bucket()
    if bucket % 12 == 0:  # ~once per hour
        return {
            "alerts": [
                {
                    "title": "Heat Advisory (Mock)",
                    "description": "High temperatures expected. This is simulated mock data.",
                    "severity": "Watch",
                    "expires_local": (
                        datetime.now(timezone.utc) + timedelta(hours=6)
                    ).strftime("%Y-%m-%dT%H:%M:%S"),
                    "regions": ["Mock Region"],
                }
            ]
        }
    return {"alerts": []}
