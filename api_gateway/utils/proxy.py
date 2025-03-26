"""
Service proxy utility for making HTTP requests to downstream services.
"""
import logging
from typing import Any

import httpx
from fastapi import Request, status
from starlette.responses import StreamingResponse

from core.config import settings
from shared.exceptions import ServiceTimeoutError, ServiceUnavailableError

logger = logging.getLogger(__name__)

# Service timeout mapping
SERVICE_TIMEOUTS = {
    "document_ingestion": settings.DOCUMENT_INGESTION_TIMEOUT,
    "document_processing": settings.DOCUMENT_PROCESSING_TIMEOUT,
    "entity_extraction": settings.ENTITY_EXTRACTION_TIMEOUT,
    "task_orchestration": settings.TASK_ORCHESTRATION_TIMEOUT,
}

# Health status tracker for circuit breaking
service_health: dict[str, str] = {}


def get_tracking_headers(request: Request | None = None) -> dict[str, str]:
    """
    Get request tracking headers from the current request.

    Args:
        request: Optional FastAPI request object

    Returns:
        Dict containing request tracking headers
    """
    headers = {}
    if request:
        if hasattr(request.state, "request_id"):
            headers["X-Request-ID"] = request.state.request_id
        if hasattr(request.state, "correlation_id"):
            headers["X-Correlation-ID"] = request.state.correlation_id
    return headers


async def proxy_request(
    service_name: str,
    method: str,
    path: str,
    *,
    request: Request | None = None,
    headers: dict | None = None,
    params: dict | None = None,
    json_data: dict | None = None,
    binary_data: bytes | None = None,
    timeout: float | None = None,
) -> httpx.Response:
    """
    Proxy a request to a downstream service with proper error handling and circuit breaking.

    Args:
        service_name: Name of the service to call
        method: HTTP method (GET, POST, etc.)
        path: Path component of the URL
        request: Optional FastAPI request object for tracking headers
        headers: Optional request headers
        params: Optional query parameters
        json_data: Optional JSON request body
        binary_data: Optional binary request body
        timeout: Optional timeout override

    Returns:
        Response from the downstream service

    Raises:
        ServiceUnavailableError: If the service is unhealthy or unreachable
        ServiceTimeoutError: If the request times out
    """
    # Check circuit breaker status
    if service_health.get(service_name) == "failed":
        logger.error(f"Circuit breaker is open for {service_name}")
        raise ServiceUnavailableError(
            service_name=service_name,
            detail="Service is currently unavailable",
        )

    # Get base URL for service
    service_url = getattr(settings, f"{service_name.upper()}_SERVICE_URL")
    if not service_url:
        raise ValueError(f"Unknown service: {service_name}")

    # Use service-specific timeout or fallback to default
    request_timeout = timeout or SERVICE_TIMEOUTS.get(
        service_name, settings.API_GATEWAY_DEFAULT_TIMEOUT
    )

    # Merge tracking headers with provided headers
    request_headers = headers or {}
    request_headers.update(get_tracking_headers(request))

    try:
        async with httpx.AsyncClient(timeout=request_timeout) as client:
            response = await client.request(
                method=method,
                url=f"{service_url}{path}",
                headers=request_headers,
                params=params,
                json=json_data,
                content=binary_data,
            )

            # Update circuit breaker status
            if response.is_success:
                service_health[service_name] = "healthy"
            elif response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
                service_health[service_name] = "failed"

            return response

    except httpx.TimeoutException as e:
        logger.error(
            f"Request to {service_name} timed out",
            extra={
                "service": service_name,
                "timeout": request_timeout,
                "error": str(e),
                **(get_tracking_headers(request) if request else {}),
            },
        )
        # Mark service as potentially unhealthy
        service_health[service_name] = "degraded"
        raise ServiceTimeoutError(
            service_name=service_name,
            detail=f"Request timed out after {request_timeout} seconds",
        )

    except httpx.HTTPError as e:
        logger.error(
            f"HTTP error when calling {service_name}",
            extra={
                "service": service_name,
                "error": str(e),
                **(get_tracking_headers(request) if request else {}),
            },
        )
        # Mark service as failed for circuit breaking
        service_health[service_name] = "failed"
        raise ServiceUnavailableError(
            service_name=service_name,
            detail=f"Service request failed: {str(e)}",
        )


async def check_service_health(service_name: str) -> dict[str, Any]:
    """
    Check the health of a specific service.

    Args:
        service_name: Name of the service to check

    Returns:
        Dict containing health status information
    """
    try:
        response = await proxy_request(
            service_name=service_name,
            method="GET",
            path="/health",
            timeout=5.0,  # Short timeout for health checks
        )

        if response.is_success:
            return {
                "status": "healthy",
                "latency_ms": round(response.elapsed.total_seconds() * 1000, 2),
            }
        else:
            return {
                "status": "unhealthy",
                "error": f"Health check failed with status {response.status_code}",
            }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }


async def stream_proxy_response(
    service_name: str,
    request: Request,
    path: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    params: dict | None = None,
    json_data: dict | None = None,
    binary_data: bytes | None = None,
    timeout: float | None = None,
) -> StreamingResponse:
    """
    Proxy a request to a target service and stream the response.
    Useful for file downloads or large responses.

    Args:
        service_name: Name of the service to call
        request: The incoming request to proxy
        path: Path component of the URL
        method: HTTP method (GET, POST, etc.)
        headers: Optional additional headers to include
        params: Optional query parameters
        json_data: Optional JSON request body
        binary_data: Optional binary request body
        timeout: Optional timeout override

    Returns:
        StreamingResponse: A streaming response from the target service

    Raises:
        ServiceUnavailableError: If the target service is unavailable
        ServiceTimeoutError: If the request to the target service times out
    """
    response = await proxy_request(
        service_name=service_name,
        method=method,
        path=path,
        request=request,
        headers=headers,
        params=params,
        json_data=json_data,
        binary_data=binary_data,
        timeout=timeout,
    )

    return StreamingResponse(
        content=response.aiter_bytes(),
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type"),
    )
