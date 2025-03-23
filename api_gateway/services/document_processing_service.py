import logging
from typing import Any

import httpx
from fastapi import status

from core.config import settings
from shared.exceptions.base import ApplicationError, ServiceUnavailableError

logger = logging.getLogger(__name__)

BASE_URL = settings.DOCUMENT_PROCESSING_SERVICE_URL
DEFAULT_TIMEOUT = settings.API_GATEWAY_DEFAULT_TIMEOUT


async def process_document(
    document_id: str, options: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Submit a document for processing.

    Args:
        document_id: ID of the document to process
        options: Optional processing options

    Returns:
        dict containing the processing job information

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/process"

    payload: dict[str, Any] = {
        "document_id": document_id,
    }

    if options:
        payload["options"] = options

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(url, json=payload)

            if response.status_code == status.HTTP_202_ACCEPTED:
                return response.json()
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error processing document: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Document Processing Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Document Processing Service",
            detail="Document Processing Service is currently unavailable",
        )


async def get_processing_status(job_id: str) -> dict[str, Any]:
    """
    Get the status of a document processing job.

    Args:
        job_id: ID of the processing job

    Returns:
        dict containing the job status information

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/process/{job_id}"

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)

            if response.status_code == status.HTTP_200_OK:
                return response.json()
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                raise ApplicationError(
                    message=f"Processing job with ID {job_id} not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error retrieving processing status: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Document Processing Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Document Processing Service",
            detail="Document Processing Service is currently unavailable",
        )


async def list_processing_jobs(
    page: int = 1,
    limit: int = 10,
    status_filter: str | None = None,
    document_id: str | None = None,
) -> dict[str, Any]:
    """
    List document processing jobs.

    Args:
        page: Page number for pagination
        limit: Number of items per page
        status_filter: Optional filter by job status
        document_id: Optional filter by document ID

    Returns:
        dict containing the list of processing jobs and pagination info

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/process"
    params: dict[str, Any] = {"page": page, "limit": limit}

    if status_filter:
        params["status"] = status_filter

    if document_id:
        params["document_id"] = document_id

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url, params=params)

            if response.status_code == status.HTTP_200_OK:
                return response.json()
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error listing processing jobs: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Document Processing Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Document Processing Service",
            detail="Document Processing Service is currently unavailable",
        )
