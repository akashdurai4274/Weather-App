"""Geocoding service using Nominatim (OpenStreetMap) - no API key required."""

import httpx
import structlog

logger = structlog.get_logger()

NOMINATIM_URL = "https://nominatim.openstreetmap.org"
HEADERS = {"User-Agent": "WeatherMonitor/1.0"}

_cache: dict[str, dict | None] = {}


async def validate_city(city: str) -> dict | None:
    """Validate city name and return location info, or None if invalid."""
    key = f"city:{city.lower().strip()}"
    if key in _cache:
        return _cache[key]

    try:
        async with httpx.AsyncClient(timeout=5, headers=HEADERS) as client:
            resp = await client.get(f"{NOMINATIM_URL}/search", params={
                "q": city,
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            })
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    r = data[0]
                    addr = r.get("address", {})
                    result = {
                        "city": addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or city.title(),
                        "country": addr.get("country_code", "xx").upper(),
                        "lat": float(r["lat"]),
                        "lon": float(r["lon"]),
                    }
                    _cache[key] = result
                    logger.info("geocoding_success", city=city, result=result)
                    return result
    except Exception as e:
        logger.warning("geocoding_error", city=city, error=str(e))

    _cache[key] = None
    return None


async def reverse_geocode(lat: float, lon: float) -> dict | None:
    """Get city name from coordinates."""
    key = f"coords:{lat:.2f},{lon:.2f}"
    if key in _cache:
        return _cache[key]

    try:
        async with httpx.AsyncClient(timeout=5, headers=HEADERS) as client:
            resp = await client.get(f"{NOMINATIM_URL}/reverse", params={
                "lat": lat,
                "lon": lon,
                "format": "json",
                "addressdetails": 1,
            })
            if resp.status_code == 200:
                data = resp.json()
                addr = data.get("address", {})
                result = {
                    "city": addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or addr.get("county") or "Unknown",
                    "country": addr.get("country_code", "xx").upper(),
                }
                _cache[key] = result
                logger.info("reverse_geocoding_success", lat=lat, lon=lon, result=result)
                return result
    except Exception as e:
        logger.warning("reverse_geocoding_error", lat=lat, lon=lon, error=str(e))

    _cache[key] = None
    return None
