"""
Proxy utilities for the API Gateway.
Provides helper functions for proxying requests to other services.
"""
import logging
from typing import Any, Optional
from urllib.parse import urljoin

import httpx
from fastapi import Request
from starlette.responses import StreamingResponse

from core.config import settings
from shared.utils.request_handler import process_async_request

logger = logging.getLogger(__name__)


async def proxy_request(
    target_url: str,
    request: Request,
    path_suffix: str = "",
    additional_headers: dict[str, str] | None = None,
    timeout: float | None = None,
) -> Any:
    """
    Proxy a request to a target service.

    Args:
        target_url: The base URL of the target service
        request: The incoming request to proxy
        path_suffix: Optional path suffix to append to the request path
        additional_headers: Optional additional headers to include
        timeout: Optional timeout override

    Returns:
        Response: The response from the target service

    Raises:
        ServiceUnavailableError: If the target service is unavailable
        ServiceTimeoutError: If the request to the target service times out
    """
    full_path = request.url.path
    if settings.API_GATEWAY_API_PREFIX and full_path.startswith(
        settings.API_GATEWAY_API_PREFIX
    ):
        full_path = full_path[len(settings.API_GATEWAY_API_PREFIX) :]

    url = urljoin(target_url, full_path + path_suffix)

    service_name = (
        target_url.split("://")[1].split(".")[0] if "://" in target_url else "unknown"
    )

    body = await request.body()

    headers = {}
    for name, value in request.headers.items():
        if name.lower() not in ("host", "content-length"):
            headers[name] = value

    if additional_headers:
        headers.update(additional_headers)

    # Add request tracking headers
    if hasattr(request.state, "request_id"):
        headers["X-Request-ID"] = request.state.request_id

    if timeout is None:
        timeout = settings.API_GATEWAY_DEFAULT_TIMEOUT

    async def make_request():
        async with httpx.AsyncClient(timeout=timeout) as client:
            return await client.request(
                method=request.method,
                url=url,
                params=request.query_params,
                headers=headers,
                content=body,
                cookies=request.cookies,
                follow_redirects=True,
            )

    return await process_async_request(
        make_request,
        error_message=f"Failed to proxy request to {service_name}",
    )


async def stream_proxy_response(
    target_url: str,
    request: Request,
    path_suffix: str = "",
    additional_headers: Optional[dict[str, str]] = None,
    timeout: float | None = None,
) -> StreamingResponse:
    """
    Proxy a request to a target service and stream the response.
    Useful for file downloads or large responses.

    Args:
        target_url: The base URL of the target service
        request: The incoming request to proxy
        path_suffix: Optional path suffix to append to the request path
        additional_headers: Optional additional headers to include
        timeout: Optional timeout override

    Returns:
        StreamingResponse: A streaming response from the target service

    Raises:
        ServiceUnavailableError: If the target service is unavailable
        ServiceTimeoutError: If the request to the target service times out
    """
    response = await proxy_request(
        target_url=target_url,
        request=request,
        path_suffix=path_suffix,
        additional_headers=additional_headers,
        timeout=timeout,
    )

    return StreamingResponse(
        content=response.aiter_bytes(),
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type"),
    )
