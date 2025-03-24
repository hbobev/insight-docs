from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    VALIDATED = "validated"


class DocumentType(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"
    FORM = "form"
    ID_CARD = "id_card"
    OTHER = "other"


class DocumentBase(BaseModel):
    filename: str
    file_size: int
    mime_type: str
    file_extension: str


class DocumentCreate(DocumentBase):
    original_filename: str
    upload_timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    status: DocumentStatus = DocumentStatus.UPLOADED
    document_type: DocumentType | None = None


class DocumentResponse(DocumentBase):
    id: str
    original_filename: str
    upload_timestamp: datetime
    status: DocumentStatus
    document_type: DocumentType | None = None
    processing_timestamp: datetime | None = None
    storage_path: str
    preview_url: str | None = None

    class Config:
        from_attributes = True


class ValidationResult(BaseModel):
    is_valid: bool
    errors: list[str] = []
    warnings: list[str] = []
    document_type: DocumentType | None = None
    confidence_score: float = 0.0


class DocumentValidationResponse(BaseModel):
    document_id: str
    validation_result: ValidationResult
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
