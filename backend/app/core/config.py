from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Weather Monitor API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = Field(
        # default="postgresql+asyncpg://postgres:root123@localhost:5432/weather_db"
        default="DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_3UHDWSsBoep0@ep-spring-band-ahziuwls-pooler.c-3.us-east-1.aws.neon.tech/neondb"
    )
    DB_ECHO: bool = False

    # JWT
    JWT_SECRET_KEY: str = Field(default="secure-production-key-use-openssl-rand-hex-32")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # WeatherBit via RapidAPI
    RAPIDAPI_KEY: str = Field(default="")
    RAPIDAPI_HOST: str = "weatherbit-com.p.rapidapi.com"
    WEATHERBIT_BASE_URL: str = "https://weatherbit-com.p.rapidapi.com"

    # External API settings
    API_TIMEOUT_SECONDS: int = 5
    API_MAX_RETRIES: int = 3

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173","http://127.0.0.1:3000"]

    # Admin
    ADMIN_SECRET_KEY: str = Field(default="admin-secret-secured-secret-key-production")

    # Default fallback city
    DEFAULT_CITY: str = "London"
    DEFAULT_COUNTRY: str = "GB"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
