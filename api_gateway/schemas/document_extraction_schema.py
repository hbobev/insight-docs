from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ExtractionStatus(str, Enum):
    """Enum for extraction job status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class EntityType(str, Enum):
    """Enum for entity types."""

    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    DATE = "date"
    MONEY = "money"
    PERCENTAGE = "percentage"
    PHONE_NUMBER = "phone_number"
    EMAIL = "email"
    URL = "url"
    CUSTOM = "custom"


class EntityValue(BaseModel):
    """Schema for entity value."""

    raw_text: str
    normalized_value: Any | None = None
    confidence: float = Field(..., ge=0.0, le=1.0)


class Entity(BaseModel):
    """Schema for extracted entity."""

    entity_type: EntityType
    value: EntityValue
    page: int | None = None
    bounding_box: dict[str, float] | None = None
    start_pos: int | None = None
    end_pos: int | None = None
    context: str | None = None
    metadata: dict[str, Any] | None = None


class ExtractionOptions(BaseModel):
    """Schema for entity extraction options."""

    entity_types: list[EntityType] | None = None
    min_confidence: float = Field(0.5, ge=0.0, le=1.0)
    include_context: bool = True
    custom_options: dict[str, Any] | None = None


class ExtractionRequest(BaseModel):
    """Schema for entity extraction request."""

    document_id: str
    options: ExtractionOptions | None = None


class ExtractionJob(BaseModel):
    """Schema for entity extraction job."""

    id: str
    document_id: str
    status: ExtractionStatus
    options: ExtractionOptions
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    progress: float | None = None


class ExtractionResult(BaseModel):
    """Schema for entity extraction result."""

    job_id: str
    document_id: str
    status: ExtractionStatus
    created_at: datetime
    completed_at: datetime | None = None
    entities: list[Entity] = []
    metadata: dict[str, Any] | None = None
    error_message: str | None = None


class EntityTypeInfo(BaseModel):
    """Schema for entity type information."""

    id: EntityType
    name: str
    description: str
    examples: list[str]


class ExtractionJobList(BaseModel):
    """Schema for list of extraction jobs response."""

    items: list[ExtractionJob]
    pagination: dict[str, Any]
