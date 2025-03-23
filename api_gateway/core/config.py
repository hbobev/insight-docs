"""
API Gateway service configuration.

This module provides the settings class for the API Gateway service.
"""
from pathlib import Path

from pydantic_settings import SettingsConfigDict

from shared.config.settings import BaseAppSettings


class ApiGatewaySettings(BaseAppSettings):
    """API Gateway service settings."""

    # Application settings
    APP_ENV: str
    DEBUG: bool
    LOG_LEVEL: str

    # Service configuration
    API_GATEWAY_PROJECT_NAME: str
    API_GATEWAY_VERSION: str
    API_GATEWAY_HOST: str
    API_GATEWAY_PORT: int
    API_GATEWAY_API_PREFIX: str
    API_GATEWAY_DEFAULT_TIMEOUT: int
    API_GATEWAY_WORKERS: int
    API_GATEWAY_CORS_ORIGINS: list[str]

    # Microservices URLs
    DOCUMENT_INGESTION_SERVICE_URL: str
    DOCUMENT_PROCESSING_SERVICE_URL: str
    ENTITY_EXTRACTION_SERVICE_URL: str
    TASK_ORCHESTRATION_SERVICE_URL: str

    # Authentication settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENABLE_AUTH: bool

    # Rate limiting
    ENABLE_RATE_LIMIT: bool
    RATE_LIMIT_MAX_REQUESTS: int
    RATE_LIMIT_WINDOW_SECONDS: int

    # Monitoring
    ENABLE_METRICS: bool
    METRICS_PORT: int

    model_config = SettingsConfigDict(
        env_file=BaseAppSettings.get_env_file(Path(__file__).parent.parent),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = ApiGatewaySettings()
