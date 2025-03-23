import logging
from typing import Any, Dict, List, Optional

import httpx
from fastapi import status

from core.config import settings
from shared.exceptions.base import ApplicationError, ServiceUnavailableError

logger = logging.getLogger(__name__)

BASE_URL = settings.ENTITY_EXTRACTION_SERVICE_URL
DEFAULT_TIMEOUT = settings.API_GATEWAY_DEFAULT_TIMEOUT


async def extract_entities(
    document_id: str, options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Submit a document for entity extraction.

    Args:
        document_id: ID of the document to extract entities from
        options: Optional extraction options

    Returns:
        Dict containing the extraction job information

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/extract"

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
                    message=f"Error extracting entities: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Entity Extraction Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Entity Extraction Service",
            detail="Entity Extraction Service is currently unavailable",
        )


async def get_extraction_result(job_id: str) -> Dict[str, Any]:
    """
    Get the result of an entity extraction job.

    Args:
        job_id: ID of the extraction job

    Returns:
        Dict containing the extraction results

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/extract/{job_id}"

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)

            if response.status_code == status.HTTP_200_OK:
                return response.json()
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                raise ApplicationError(
                    message=f"Extraction job with ID {job_id} not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error retrieving extraction results: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Entity Extraction Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Entity Extraction Service",
            detail="Entity Extraction Service is currently unavailable",
        )


async def get_entity_types() -> List[Dict[str, Any]]:
    """
    Get the list of supported entity types.

    Returns:
        List of supported entity types with their descriptions

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/entity-types"

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)

            if response.status_code == status.HTTP_200_OK:
                return response.json()
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error retrieving entity types: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Entity Extraction Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Entity Extraction Service",
            detail="Entity Extraction Service is currently unavailable",
        )
