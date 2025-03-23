from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ServiceHealth(BaseModel):
    """Schema for service health information."""

    status: str
    url: str
    version: str | None = None
    details: dict[str, Any] | None = None


class SystemInfo(BaseModel):
    """Schema for system information."""

    platform: str
    python_version: str
    processor: str


class MemoryInfo(BaseModel):
    """Schema for memory information."""

    total: int | None = None
    available: int | None = None
    percent_used: float | None = None
    error: str | None = None


class ApiGatewayStats(BaseModel):
    """Schema for API Gateway statistics."""

    version: str
    uptime: str
    start_time: datetime
    request_count: int
    error_count: int


class SystemStats(BaseModel):
    """Schema for system statistics."""

    api_gateway: ApiGatewayStats
    system: SystemInfo
    memory: MemoryInfo
    services: dict[str, ServiceHealth]
