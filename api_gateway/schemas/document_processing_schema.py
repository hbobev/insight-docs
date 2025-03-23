from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class ProcessingStatus(str, Enum):
    """Enum for processing job status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingOptions(BaseModel):
    """Schema for document processing options."""

    ocr_enabled: bool = True
    language: str | None = None
    enhance_image: bool = False
    extract_tables: bool = True
    extract_text: bool = True
    extract_forms: bool = False
    custom_options: dict[str, Any] | None = None


class ProcessingRequest(BaseModel):
    """Schema for document processing request."""

    document_id: str
    options: ProcessingOptions | None = None


class ProcessingJob(BaseModel):
    """Schema for document processing job."""

    id: str
    document_id: str
    status: ProcessingStatus
    options: ProcessingOptions
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    progress: float | None = None
    result_url: str | None = None


class ProcessingResult(BaseModel):
    """Schema for document processing result."""

    job_id: str
    document_id: str
    status: ProcessingStatus
    created_at: datetime
    completed_at: datetime | None = None
    pages: list[dict[str, Any]] | None = None
    text_content: str | None = None
    tables: list[dict[str, Any]] | None = None
    forms: list[dict[str, Any]] | None = None
    metadata: dict[str, Any] | None = None
    error_message: str | None = None


class ProcessingJobList(BaseModel):
    """Schema for list of processing jobs response."""

    items: list[ProcessingJob]
    pagination: dict[str, Any]
