import logging
from typing import Any

import httpx
from fastapi import status

from core.config import settings
from shared.exceptions.base import ApplicationError, ServiceUnavailableError

logger = logging.getLogger(__name__)

BASE_URL = settings.TASK_ORCHESTRATION_SERVICE_URL
DEFAULT_TIMEOUT = settings.API_GATEWAY_DEFAULT_TIMEOUT


async def create_workflow(
    document_id: str,
    workflow_type: str,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a new workflow for a document.

    Args:
        document_id: ID of the document
        workflow_type: Type of workflow to create
        config: Optional workflow configuration

    Returns:
        Dict containing the created workflow information

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/workflows"

    payload: dict[str, Any] = {
        "document_id": document_id,
        "workflow_type": workflow_type,
    }

    if config:
        payload["config"] = config

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(url, json=payload)

            if response.status_code == status.HTTP_201_CREATED:
                return response.json()
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error creating workflow: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Task Orchestration Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Task Orchestration Service",
            detail="Task Orchestration Service is currently unavailable",
        )


async def get_workflow(workflow_id: str) -> dict[str, Any]:
    """
    Get workflow details.

    Args:
        workflow_id: ID of the workflow to retrieve

    Returns:
        Dict containing the workflow information

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/workflows/{workflow_id}"

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)

            if response.status_code == status.HTTP_200_OK:
                return response.json()
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                raise ApplicationError(
                    message=f"Workflow with ID {workflow_id} not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error retrieving workflow: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Task Orchestration Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Task Orchestration Service",
            detail="Task Orchestration Service is currently unavailable",
        )


async def list_workflows(
    page: int = 1,
    limit: int = 10,
    status_filter: str | None = None,
    document_id: str | None = None,
) -> dict[str, Any]:
    """
    List workflows.

    Args:
        page: Page number for pagination
        limit: Number of items per page
        status_filter: Optional filter by workflow status
        document_id: Optional filter by document ID

    Returns:
        Dict containing the list of workflows and pagination info

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/workflows"
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
                    message=f"Error listing workflows: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Task Orchestration Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Task Orchestration Service",
            detail="Task Orchestration Service is currently unavailable",
        )


async def get_workflow_types() -> list[dict[str, Any]]:
    """
    Get the list of supported workflow types.

    Returns:
        List of supported workflow types with their descriptions

    Raises:
        ServiceUnavailableError: If the service is unavailable
        ApplicationError: If there's an error with the request
    """
    url = f"{BASE_URL}/api/v1/workflow-types"

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)

            if response.status_code == status.HTTP_200_OK:
                return response.json()
            else:
                error_detail = response.json().get("detail", {})
                error_message = error_detail.get("error", "Unknown error")
                raise ApplicationError(
                    message=f"Error retrieving workflow types: {error_message}",
                    status_code=response.status_code,
                )
    except httpx.RequestError as exc:
        logger.error(f"Error connecting to Task Orchestration Service: {exc}")
        raise ServiceUnavailableError(
            service_name="Task Orchestration Service",
            detail="Task Orchestration Service is currently unavailable",
        )
