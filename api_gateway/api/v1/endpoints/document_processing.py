import logging
from typing import Any

from fastapi import APIRouter, Body, Query, status

from services import document_processing_service
from shared.utils.request_handler import process_async_request

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/",
    summary="Process a document",
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Document processing job created",
)
async def process_document(
    document_id: str = Body(..., embed=True),
    options: dict[str, Any] | None = Body(None, embed=True),
):
    """
    Submit a document for processing.

    Args:
        document_id: ID of the document to process
        options: Optional processing options

    Returns:
        Processing job information
    """

    async def request_handler():
        return await document_processing_service.process_document(
            document_id=document_id,
            options=options,
        )

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_202_ACCEPTED,
        error_message="Failed to process document",
    )


@router.get(
    "/{job_id}",
    summary="Get processing job status",
    status_code=status.HTTP_200_OK,
    response_description="Processing job status",
)
async def get_processing_status(job_id: str):
    """
    Get the status of a document processing job.

    Args:
        job_id: ID of the processing job

    Returns:
        Processing job status
    """

    async def request_handler():
        return await document_processing_service.get_processing_status(job_id)

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message=f"Processing job with ID {job_id} not found",
    )


@router.get(
    "/",
    summary="List processing jobs",
    status_code=status.HTTP_200_OK,
    response_description="List of processing jobs",
)
async def list_processing_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    status_filter: str | None = Query(None, description="Filter by job status"),
    document_id: str | None = Query(None, description="Filter by document ID"),
):
    """
    List document processing jobs with pagination and filtering options.

    Args:
        page: Page number for pagination
        limit: Number of items per page
        status_filter: Optional filter by job status
        document_id: Optional filter by document ID

    Returns:
        List of processing jobs and pagination information
    """

    async def request_handler():
        return await document_processing_service.list_processing_jobs(
            page=page,
            limit=limit,
            status_filter=status_filter,
            document_id=document_id,
        )

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message="Failed to list processing jobs",
    )
