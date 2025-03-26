"""
Task Orchestration service configuration.

This module provides the settings class for the Task Orchestration service.
"""
from pathlib import Path

from pydantic_settings import SettingsConfigDict

from shared.config.settings import BaseAppSettings


class TaskOrchestrationSettings(BaseAppSettings):
    """Task Orchestration service settings."""

    # Application settings
    APP_ENV: str
    DEBUG: bool
    LOG_LEVEL: str

    # Service Configuration
    SERVICE_HOST: str
    SERVICE_PORT: int = 8004
    SERVICE_WORKERS: int = 1

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "InsightDocs Task Orchestration Service"
    CORS_ORIGINS: list[str]

    # Queue settings
    RABBITMQ_URI: str

    # Service connections
    DOCUMENT_PROCESSING_SERVICE_URL: str
    DOCUMENT_INGESTION_SERVICE_URL: str
    ENTITY_EXTRACTION_SERVICE_URL: str

    model_config = SettingsConfigDict(
        env_file=BaseAppSettings.get_env_file(Path(__file__).parent.parent),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = TaskOrchestrationSettings()
