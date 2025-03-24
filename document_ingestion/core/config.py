from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.config.settings import BaseAppSettings


class Settings(BaseSettings):
    """Service-specific settings."""

    APP_ENV: str
    DEBUG: bool
    LOG_LEVEL: str

    SERVICE_PORT: int
    SERVICE_HOST: str
    SERVICE_WORKERS: int

    API_V1_PREFIX: str
    PROJECT_NAME: str

    UPLOAD_FOLDER: str
    MAX_CONTENT_LENGTH: int
    ALLOWED_EXTENSIONS: list[str]

    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DATABASE: str
    MONGO_COLLECTION: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_URI: str

    MIN_IMAGE_RESOLUTION: int
    MAX_IMAGE_SIZE: int

    CORS_ORIGINS: list[str]

    model_config = SettingsConfigDict(
        env_file=BaseAppSettings.get_env_file(Path(__file__).parent.parent),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
