from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class WorkflowStatus(str, Enum):
    """Enum for workflow status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class WorkflowType(str, Enum):
    """Enum for workflow types."""

    DOCUMENT_PROCESSING = "document_processing"
    ENTITY_EXTRACTION = "entity_extraction"
    DOCUMENT_CLASSIFICATION = "document_classification"
    CUSTOM = "custom"


class TaskStatus(str, Enum):
    """Enum for task status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Task(BaseModel):
    """Schema for workflow task."""

    id: str
    name: str
    task_type: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    result: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None


class WorkflowConfig(BaseModel):
    """Schema for workflow configuration."""

    tasks: list[dict[str, Any]] | None = None
    parallel_execution: bool = False
    retry_failed: bool = True
    max_retries: int = 3
    timeout_seconds: int | None = None
    notification_email: str | None = None
    custom_config: dict[str, Any] | None = None


class WorkflowRequest(BaseModel):
    """Schema for workflow creation request."""

    document_id: str
    workflow_type: WorkflowType
    config: WorkflowConfig | None = None


class Workflow(BaseModel):
    """Schema for workflow."""

    id: str
    document_id: str
    workflow_type: WorkflowType
    status: WorkflowStatus
    config: WorkflowConfig
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    progress: float | None = None
    tasks: list[Task] = []
    result_summary: dict[str, Any] | None = None


class WorkflowTypeInfo(BaseModel):
    """Schema for workflow type information."""

    id: WorkflowType
    name: str
    description: str
    available_tasks: list[str]
    default_config: dict[str, Any] | None = None


class WorkflowList(BaseModel):
    """Schema for list of workflows response."""

    items: list[Workflow]
    pagination: dict[str, Any]
