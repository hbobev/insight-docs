from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""

    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(10, ge=1, le=100, description="Items per page")


class PaginationInfo(BaseModel):
    """Schema for pagination information."""

    page: int
    limit: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Schema for paginated response."""

    items: list[T]
    pagination: PaginationInfo


class ErrorDetail(BaseModel):
    """Schema for error details."""

    error: str
    code: str | None = None
    message: str | None = None


class ErrorResponse(BaseModel):
    """Schema for error response."""

    detail: ErrorDetail


class SuccessResponse(BaseModel):
    """Schema for success response."""

    data: Any
    metadata: dict[str, Any] | None = None
