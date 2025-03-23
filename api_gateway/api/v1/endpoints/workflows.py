import logging
from typing import Any

from fastapi import APIRouter, Body, Query, status

from services import workflow_service
from shared.utils.request_handler import process_async_request

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/",
    summary="Create a workflow",
    status_code=status.HTTP_201_CREATED,
    response_description="Workflow created successfully",
)
async def create_workflow(
    document_id: str = Body(..., embed=True),
    workflow_type: str = Body(..., embed=True),
    config: dict[str, Any] | None = Body(None, embed=True),
):
    async def request_handler():
        return await workflow_service.create_workflow(
            document_id=document_id,
            workflow_type=workflow_type,
            config=config,
        )

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_201_CREATED,
        error_message="Failed to create workflow",
    )


@router.get(
    "/{workflow_id}",
    summary="Get workflow details",
    status_code=status.HTTP_200_OK,
    response_description="Workflow details",
)
async def get_workflow(workflow_id: str):
    async def request_handler():
        return await workflow_service.get_workflow(workflow_id)

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message=f"Workflow with ID {workflow_id} not found",
    )


@router.get(
    "/",
    summary="List workflows",
    status_code=status.HTTP_200_OK,
    response_description="List of workflows",
)
async def list_workflows(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    status_filter: str | None = Query(None, description="Filter by workflow status"),
    document_id: str | None = Query(None, description="Filter by document ID"),
):
    async def request_handler():
        return await workflow_service.list_workflows(
            page=page,
            limit=limit,
            status_filter=status_filter,
            document_id=document_id,
        )

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message="Failed to list workflows",
    )


@router.get(
    "/types",
    summary="Get workflow types",
    status_code=status.HTTP_200_OK,
    response_description="List of workflow types",
)
async def get_workflow_types():
    async def request_handler():
        return await workflow_service.get_workflow_types()

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message="Failed to retrieve workflow types",
    )
