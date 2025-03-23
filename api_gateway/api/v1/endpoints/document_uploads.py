import logging

from fastapi import APIRouter, File, Form, Query, UploadFile, status

from services import document_upload_service
from shared.utils.request_handler import process_async_request

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/",
    summary="Upload a document",
    status_code=status.HTTP_201_CREATED,
    response_description="Document uploaded successfully",
)
async def upload_document(
    file: UploadFile = File(...),
    metadata: str | None = Form(None),
):
    async def request_handler():
        file_content = await file.read()
        return await document_upload_service.upload_document(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type,
            metadata=metadata,
        )

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_201_CREATED,
        error_message="Failed to upload document",
    )


@router.get(
    "/{document_id}",
    summary="Get document details",
    status_code=status.HTTP_200_OK,
    response_description="Document details",
)
async def get_document(document_id: str):
    async def request_handler():
        return await document_upload_service.get_document(document_id)

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message=f"Document with ID {document_id} not found",
    )


@router.get(
    "/",
    summary="List documents",
    status_code=status.HTTP_200_OK,
    response_description="List of documents",
)
async def list_documents(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    status_filter: str | None = Query(None, description="Filter by document status"),
    document_type: str | None = Query(None, description="Filter by document type"),
):
    async def request_handler():
        return await document_upload_service.list_documents(
            page=page,
            limit=limit,
            status_filter=status_filter,
            document_type=document_type,
        )

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message="Failed to list documents",
    )
