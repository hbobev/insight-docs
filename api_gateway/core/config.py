from pathlib import Path

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).parents[3]


class Settings(BaseSettings):
    """Service-specific settings."""

    PROJECT_NAME: str = ""
    VERSION: str = "0.1.0"
    API_GATEWAY_HOST: str
    API_GATEWAY_PORT: int
    API_GATEWAY_CORS_ORIGINS: list[AnyHttpUrl]
    DEBUG: bool

    @field_validator("API_GATEWAY_CORS_ORIGINS")
    def validate_cors_origins(cls, v: list[str]) -> list[AnyHttpUrl] | list[str]:
        """Validate that CORS origins are valid URLs or use default origins when given as a string."""
        if isinstance(v, str) and not v.startswith("["):
            return [AnyHttpUrl(url=origin.strip()) for origin in v.split(",") if origin]
        if isinstance(v, list):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = str(ROOT_DIR / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
