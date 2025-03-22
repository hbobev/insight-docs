"""
Shared configuration utilities for the InsightDocs services.

This module provides base classes and utilities that can be used by
individual microservices to implement their own configuration.
"""
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Base settings class that can be extended by each microservice.

    This provides common utilities and patterns but doesn't contain
    specific configuration values.
    """

    @classmethod
    def get_env_file(cls, service_dir: Path) -> list[Path]:
        """
        Get the environment file for the service.

        Args:
            service_dir: Directory of the service

        Returns:
            List containing path to the service's .env file if it exists
        """
        env_file = service_dir / ".env"
        return [env_file] if env_file.exists() else []

    @field_validator("LOG_LEVEL", mode="before", check_fields=False)
    def validate_log_level(cls, v: str) -> str:
        """Validate log level values."""
        allowed = ["debug", "info", "warning", "error", "critical"]
        if v.lower() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {', '.join(allowed)}")
        return v.lower()


def build_mongodb_connection_string(
    host: str, port: int, database: str, username: str, password: str
) -> str:
    """Build a MongoDB connection string from individual components."""
    return f"mongodb://{username}:{password}@{host}:{port}/{database}"


def build_postgres_connection_string(
    host: str, port: int, database: str, username: str, password: str
) -> str:
    """Build a PostgreSQL connection string from individual components."""
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"


def build_redis_connection_string(
    host: str, port: int, db: int, password: str | None = None
) -> str:
    """Build a Redis connection string from individual components."""
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    return f"redis://{host}:{port}/{db}"


def build_rabbitmq_connection_string(
    host: str, port: int, username: str, password: str, vhost: str = "/"
) -> str:
    """Build a RabbitMQ connection string from individual components."""
    # Make sure vhost starts with a slash
    if not vhost.startswith("/"):
        vhost = f"/{vhost}"

    return f"amqp://{username}:{password}@{host}:{port}{vhost}"
