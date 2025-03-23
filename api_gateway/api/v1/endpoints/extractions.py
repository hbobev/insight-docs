import logging
from typing import Any

from fastapi import APIRouter, Body, Query, status

from services import entity_extraction_service
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
    async def request_handler():
        return await entity_extraction_service.process_document(
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
    async def request_handler():
        return await entity_extraction_service.get_processing_status(job_id)

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
    async def request_handler():
        return await entity_extraction_service.list_processing_jobs(
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
