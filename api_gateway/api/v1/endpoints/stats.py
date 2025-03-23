import logging
import platform
import time
from datetime import datetime, timedelta

from fastapi import APIRouter, status

from core.config import settings
from shared.utils.request_handler import process_async_request

router = APIRouter()
logger = logging.getLogger(__name__)

start_time = time.time()
request_count = 0
error_count = 0


@router.get(
    "/",
    summary="Get system statistics",
    status_code=status.HTTP_200_OK,
    response_description="System statistics",
)
async def get_system_stats():
    async def request_handler():
        global request_count
        request_count += 1

        uptime_seconds = time.time() - start_time
        uptime = str(timedelta(seconds=int(uptime_seconds)))

        system_info = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
        }

        try:
            import psutil

            memory = psutil.virtual_memory()
            memory_info = {
                "total": memory.total,
                "available": memory.available,
                "percent_used": memory.percent,
            }
        except ImportError:
            memory_info = {"error": "psutil not available"}

        services_health = await _get_services_health()

        return {
            "api_gateway": {
                "version": settings.API_GATEWAY_VERSION,
                "uptime": uptime,
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "request_count": request_count,
                "error_count": error_count,
            },
            "system": system_info,
            "memory": memory_info,
            "services": services_health,
        }

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message="Failed to retrieve system statistics",
    )


async def _get_services_health() -> dict:
    """
    Get health status of all services.

    Returns:
        Dict containing health status of all services
    """
    # This is a simplified version - in a real implementation,
    # we would need to make actual requests to the services

    services = {
        "document_ingestion": {
            "status": "healthy",
            "url": settings.DOCUMENT_INGESTION_SERVICE_URL,
        },
        "document_processing": {
            "status": "healthy",
            "url": settings.DOCUMENT_PROCESSING_SERVICE_URL,
        },
        "entity_extraction": {
            "status": "healthy",
            "url": settings.ENTITY_EXTRACTION_SERVICE_URL,
        },
        "task_orchestration": {
            "status": "healthy",
            "url": settings.TASK_ORCHESTRATION_SERVICE_URL,
        },
    }

    return services
