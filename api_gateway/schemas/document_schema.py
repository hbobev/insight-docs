from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, HttpUrl


class DocumentStatus(str, Enum):
    """Enum for document status."""

    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    ARCHIVED = "archived"


class DocumentType(str, Enum):
    """Enum for document types."""

    INVOICE = "invoice"
    RECEIPT = "receipt"
    CONTRACT = "contract"
    FORM = "form"
    ID_CARD = "id_card"
    OTHER = "other"


class DocumentMetadata(BaseModel):
    """Schema for document metadata."""

    original_filename: str
    content_type: str
    size_bytes: int
    page_count: int | None = None
    language: str | None = None
    source: str | None = None
    custom_metadata: dict[str, Any] | None = None


class DocumentBase(BaseModel):
    """Base schema for document data."""

    document_type: DocumentType = DocumentType.OTHER
    status: DocumentStatus = DocumentStatus.PENDING
    metadata: DocumentMetadata


class DocumentCreate(BaseModel):
    """Schema for document creation request."""

    document_type: DocumentType | None = DocumentType.OTHER
    metadata: dict[str, Any] | None = None


class DocumentUpdate(BaseModel):
    """Schema for document update request."""

    document_type: DocumentType | None = None
    status: DocumentStatus | None = None
    metadata: dict[str, Any] | None = None


class DocumentInDB(DocumentBase):
    """Schema for document data stored in the database."""

    id: str
    file_path: str
    created_at: datetime
    updated_at: datetime
    user_id: str | None = None


class DocumentResponse(DocumentBase):
    """Schema for document data in responses."""

    id: str
    created_at: datetime
    updated_at: datetime
    download_url: HttpUrl | None = None
    preview_url: HttpUrl | None = None
    user_id: str | None = None

    class Config:
        from_attributes = True


class DocumentList(BaseModel):
    """Schema for list of documents response."""

    items: list[DocumentResponse]
    pagination: dict[str, Any]
