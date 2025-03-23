import logging
from typing import Any

import httpx
from fastapi import status

from core.config import settings
from shared.exceptions.base import ApplicationError, ServiceUnavailableError

logger = logging.getLogger(__name__)

BASE_URL = settings.DOCUMENT_INGESTION_SERVICE_URL
DEFAULT_TIMEOUT = settings.API_GATEWAY_DEFAULT_TIMEOUT


async def upload_document(
    file_content: bytes,
    filename: str,
    content_type: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Upload a document to the Document Ingestion Service.

    Args:
        file_content: Binary content of the file
        filename: Name of the file
        content_type: MIME type of the file
        metadata: Optional metadata for the document

    Returns:
        dict containing the uploaded document information

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/documents"

    files = {"file": (filename, file_content, content_type)}
    data = {}

    if metadata:
        data["metadata"] = metadata

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(url, files=files, data=data)

            if response.status_code == status.HTTP_201_CREATED:
                return response.json()
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error uploading document: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Document Ingestion Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Document Ingestion Service",
            detail="Document Ingestion Service is currently unavailable",
        )


async def get_document(document_id: str) -> dict[str, Any]:
    """
    Get document details from the Document Ingestion Service.

    Args:
        document_id: ID of the document to retrieve

    Returns:
        dict containing the document information

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/documents/{document_id}"

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)

            if response.status_code == status.HTTP_200_OK:
                return response.json()
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                raise ApplicationError(
                    message=f"Document with ID {document_id} not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error retrieving document: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Document Ingestion Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Document Ingestion Service",
            detail="Document Ingestion Service is currently unavailable",
        )


async def list_documents(
    page: int = 1,
    limit: int = 10,
    status_filter: str | None = None,
    document_type: str | None = None,
) -> dict[str, Any]:
    """
    List documents from the Document Ingestion Service.

    Args:
        page: Page number for pagination
        limit: Number of items per page
        status_filter: Optional filter by document status
        document_type: Optional filter by document type

    Returns:
        dict containing the list of documents and pagination info

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/documents"
    params: dict[str, Any] = {"page": page, "limit": limit}

    if status_filter:
        params["status"] = status_filter

    if document_type:
        params["type"] = document_type

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url, params=params)

            if response.status_code == status.HTTP_200_OK:
                return response.json()
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error listing documents: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Document Ingestion Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Document Ingestion Service",
            detail="Document Ingestion Service is currently unavailable",
        )
