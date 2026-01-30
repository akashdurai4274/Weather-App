from pydantic import BaseModel, Field


class AddWatchlistRequest(BaseModel):
    city_name: str = Field(min_length=1, max_length=100)
    country_code: str | None = Field(None, max_length=10)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)


class WatchlistLocationResponse(BaseModel):
    id: str
    city_name: str
    country_code: str | None
    latitude: float | None
    longitude: float | None

    model_config = {"from_attributes": True}


class WatchlistItemResponse(BaseModel):
    id: str
    location: WatchlistLocationResponse
    added_at: str

    model_config = {"from_attributes": True}


class WatchlistResponse(BaseModel):
    items: list[WatchlistItemResponse]
    count: int
