from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Location


class LocationRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_city(self, city_name: str) -> Location | None:
        stmt = select(Location).where(Location.city_name == city_name)
        result = await self._db.execute(stmt)
        return result.scalars().first()

    async def create(self, location: Location) -> Location:
        self._db.add(location)
        await self._db.flush()
        return location

    async def get_or_create(
        self, city_name: str, country_code: str | None = None,
        latitude: float | None = None, longitude: float | None = None,
    ) -> Location:
        existing = await self.get_by_city(city_name)
        if existing:
            return existing
        location = Location(
            city_name=city_name,
            country_code=country_code,
            latitude=latitude,
            longitude=longitude,
        )
        return await self.create(location)
