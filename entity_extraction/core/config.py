"""
Entity Extraction service configuration.

This module provides the settings class for the Entity Extraction service.
"""
from pathlib import Path

from pydantic_settings import SettingsConfigDict

from shared.config.settings import BaseAppSettings


class EntityExtractionSettings(BaseAppSettings):
    """Entity Extraction service settings."""

    # Application settings
    APP_ENV: str
    DEBUG: bool
    LOG_LEVEL: str

    # Service Configuration
    SERVICE_HOST: str
    SERVICE_PORT: int = 8003
    SERVICE_WORKERS: int = 1

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "InsightDocs Entity Extraction Service"
    CORS_ORIGINS: list[str]

    # Model settings
    MODEL_PATH: str = "data/models/entity_extractor"

    # Performance settings
    BATCH_SIZE: int = 32
    MAX_SEQUENCE_LENGTH: int = 512

    model_config = SettingsConfigDict(
        env_file=BaseAppSettings.get_env_file(Path(__file__).parent.parent),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = EntityExtractionSettings()
