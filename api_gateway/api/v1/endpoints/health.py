import logging

import httpx
from fastapi import APIRouter, status

from core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/",
    summary="Check API Gateway health",
    status_code=status.HTTP_200_OK,
    response_description="Health status of the API Gateway",
)
async def health_check() -> dict:
    """
    Check if the API Gateway is healthy.

    Returns:
        dict: Health status information
    """
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
async def services_health() -> dict:
    """
    Check the health of all dependent services.

    Returns:
        dict: Health status of all services
    """
    services: dict = {
        "document_ingestion": settings.DOCUMENT_INGESTION_SERVICE_URL,
        "document_processing": settings.DOCUMENT_PROCESSING_SERVICE_URL,
        "entity_extraction": settings.ENTITY_EXTRACTION_SERVICE_URL,
        "task_orchestration": settings.TASK_ORCHESTRATION_SERVICE_URL,
    }

    results: dict = {
        "status": "healthy",
        "services": {},
    }

    async with httpx.AsyncClient(
        timeout=settings.API_GATEWAY_DEFAULT_TIMEOUT
    ) as client:
        for service_name, service_url in services.items():
            try:
                health_endpoint = f"{service_url}/api/health"
                response = await client.get(health_endpoint)

                if response.status_code == 200:
                    results["services"][service_name] = {
                        "status": "healthy",
                        "details": response.json(),
                    }
                else:
                    results["services"][service_name] = {
                        "status": "unhealthy",
                        "details": f"Status code: {response.status_code}",
                    }
                    results["status"] = "degraded"
            except httpx.RequestError as exc:
                logger.error(f"Error checking {service_name} health: {exc}")
                results["services"][service_name] = {
                    "status": "unreachable",
                    "details": str(exc),
                }
                results["status"] = "degraded"

    return results
