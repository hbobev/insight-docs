import logging
from typing import Any

from fastapi import APIRouter, status

from core.config import settings
from utils.proxy import check_service_health

router = APIRouter()
logger = logging.getLogger(__name__)

SERVICES = [
    "document_ingestion",
    "document_processing",
    "entity_extraction",
    "task_orchestration",
]


@router.get(
    "/",
    summary="Check API Gateway health",
    status_code=status.HTTP_200_OK,
    response_description="Health status of the API Gateway",
)
async def health_check() -> dict:
    """Check API Gateway health."""
    return {
        "status": "healthy",
        "service": "api_gateway",
        "version": settings.API_GATEWAY_VERSION,
    }


@router.get(
    "/services",
    summary="Check health of all services",
    status_code=status.HTTP_200_OK,
    response_description="Health status of all services",
)
async def services_health() -> dict[str, Any]:
    """
    Check health of all dependent services.

    Returns:
        Dict with health status of each service
    """
    health_status = {}

    for service_name in SERVICES:
        health_status[service_name] = await check_service_health(service_name)

    critical_services = {"document_ingestion", "document_processing"}
    critical_services_healthy = all(
        health_status.get(service, {}).get("status") == "healthy"
        for service in critical_services
    )

    return {
        "api_gateway": {
            "status": "healthy",
            "version": settings.API_GATEWAY_VERSION,
        },
        "services": health_status,
        "overall_status": "healthy" if critical_services_healthy else "degraded",
    }
