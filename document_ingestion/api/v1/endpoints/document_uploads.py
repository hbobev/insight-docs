from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from schemas.document_schema import DocumentResponse
from services.document_service import DocumentService
from shared.utils.request_handler import process_async_request

router = APIRouter()


def get_document_service() -> DocumentService:
    return DocumentService()


@router.post(
    "/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED
)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
):
    async def request_handler():
        return await document_service.upload_document(file)

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_201_CREATED,
        error_message="Failed to upload document",
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str, document_service: DocumentService = Depends(get_document_service)
):
    async def request_handler():
        return document_service.get_document(document_id)

    return await process_async_request(
        request_handler=request_handler,
        error_message=f"Document with ID {document_id} not found",
    )


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    document_service: DocumentService = Depends(get_document_service),
):
    async def request_handler():
        return document_service.list_documents(skip=skip, limit=limit)

    return await process_async_request(
        request_handler=request_handler, error_message="Failed to retrieve documents"
    )
