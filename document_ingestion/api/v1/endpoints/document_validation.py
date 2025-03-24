from fastapi import APIRouter, Depends

from schemas.document_schema import DocumentValidationResponse
from services.document_service import DocumentService
from shared.utils.request_handler import process_async_request

router = APIRouter()


def get_document_service() -> DocumentService:
    return DocumentService()


@router.post("/{document_id}/validate")
async def validate_document(
    document_id: str, document_service: DocumentService = Depends(get_document_service)
):
    async def request_handler():
        validation_result = document_service.validate_document(document_id)
        return DocumentValidationResponse(
            document_id=document_id, validation_result=validation_result
        )

    return await process_async_request(
        request_handler=request_handler,
        error_message=f"Failed to validate document with ID {document_id}",
    )
