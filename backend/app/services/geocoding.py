"""Geocoding service using LocationIQ API for city validation and reverse geocoding."""

import httpx
import structlog
from app.core.config import settings

logger = structlog.get_logger()

LOCATIONIQ_BASE = "https://us1.locationiq.com/v1"


async def validate_city(city: str) -> dict | None:
    """Validate city name and return location info, or None if invalid."""
    if not settings.GEOCODING_API_KEY:
        return None
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{LOCATIONIQ_BASE}/search", params={
                "key": settings.GEOCODING_API_KEY,
                "q": city,
                "format": "json",
                "limit": 1,
            })
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    r = data[0]
                    addr = r.get("address", {})
                    return {
                        "city": addr.get("city") or addr.get("town") or addr.get("village") or r.get("display_name", "").split(",")[0],
                        "country": addr.get("country_code", "XX").upper(),
                        "lat": float(r["lat"]),
                        "lon": float(r["lon"]),
                    }
    except Exception as e:
        logger.warning("geocoding_error", error=str(e))
    return None


async def reverse_geocode(lat: float, lon: float) -> dict | None:
    """Get city name from coordinates."""
    if not settings.GEOCODING_API_KEY:
        return None
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{LOCATIONIQ_BASE}/reverse", params={
                "key": settings.GEOCODING_API_KEY,
                "lat": lat,
                "lon": lon,
                "format": "json",
            })
            if resp.status_code == 200:
                data = resp.json()
                addr = data.get("address", {})
                return {
                    "city": addr.get("city") or addr.get("town") or addr.get("village") or addr.get("county") or "Unknown",
                    "country": addr.get("country_code", "XX").upper(),
                }
    except Exception as e:
        logger.warning("reverse_geocoding_error", error=str(e))
    return None
