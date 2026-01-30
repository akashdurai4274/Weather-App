from pydantic import BaseModel, Field


class WeatherQuery(BaseModel):
    city: str | None = None
    lat: float | None = Field(None, ge=-90, le=90)
    lon: float | None = Field(None, ge=-180, le=180)


class CurrentWeatherData(BaseModel):
    city_name: str
    country_code: str
    temp: float
    feels_like: float
    humidity: int
    wind_speed: float
    wind_direction: str
    description: str
    icon: str
    visibility: float | None = None
    pressure: float | None = None
    uv_index: float | None = None
    clouds: int | None = None
    sunrise: str | None = None
    sunset: str | None = None
    aqi: float | None = None
    lat: float
    lon: float


class HourlyForecast(BaseModel):
    timestamp: str
    temp: float
    feels_like: float | None = None
    humidity: int | None = None
    wind_speed: float | None = None
    description: str
    icon: str
    pop: float | None = None  # probability of precipitation


class DailyForecast(BaseModel):
    date: str
    temp_high: float
    temp_low: float
    humidity: int | None = None
    wind_speed: float | None = None
    description: str
    icon: str
    pop: float | None = None


class WeatherAlert(BaseModel):
    title: str
    description: str
    severity: str | None = None
    expires: str | None = None
    regions: list[str] = []


class ForecastResponse(BaseModel):
    city_name: str
    country_code: str
    lat: float
    lon: float
    daily: list[DailyForecast] = []
    hourly: list[HourlyForecast] = []
    alerts: list[WeatherAlert] = []
    data_source: str = "live"


class CurrentWeatherResponse(BaseModel):
    data: CurrentWeatherData
    data_source: str = "live"
