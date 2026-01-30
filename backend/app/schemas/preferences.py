from pydantic import BaseModel, Field


class UpdatePreferencesRequest(BaseModel):
    default_city: str | None = Field(None, max_length=100)
    default_country: str | None = Field(None, max_length=10)
    default_lat: str | None = Field(None, max_length=20)
    default_lon: str | None = Field(None, max_length=20)
    units: str | None = Field(None, pattern=r"^(metric|imperial)$")


class PreferencesResponse(BaseModel):
    default_city: str | None
    default_country: str | None
    default_lat: str | None
    default_lon: str | None
    units: str

    model_config = {"from_attributes": True}
