from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """Token schema for authentication responses."""

    access_token: str
    token_type: str
    refresh_token: str | None = None


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""

    sub: str  # Subject (user ID)
    exp: datetime  # Expiration time
    type: str | None = "access"  # Token type (access or refresh)
    iat: datetime | None = None  # Issued at
    jti: str | None = None  # JWT ID


class UserLogin(BaseModel):
    """Schema for user login request."""

    username: str
    password: str


class TokenRefresh(BaseModel):
    """Schema for token refresh request."""

    refresh_token: str


class UserBase(BaseModel):
    """Base schema for user data."""

    username: str
    email: EmailStr
    role: str = "user"
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for user creation request."""

    password: str = Field(..., min_length=8)
    additional_data: dict[str, Any] | None = None


class UserUpdate(BaseModel):
    """Schema for user update request."""

    username: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)
    role: str | None = None
    is_active: bool | None = None
    additional_data: dict[str, Any] | None = None


class UserInDB(UserBase):
    """Schema for user data stored in the database."""

    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime


class UserResponse(UserBase):
    """Schema for user data in responses."""

    id: str
    created_at: datetime
    updated_at: datetime
    additional_data: dict[str, Any] | None = None

    class Config:
        from_attributes = True
