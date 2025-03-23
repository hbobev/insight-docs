import logging
from datetime import datetime, timezone
from typing import Any

from schemas.authentication_schema import UserInDB, UserResponse, UserUpdate
from schemas.common_schema import PaginationInfo
from services import authentication_service
from shared.exceptions.base import NotFoundError

logger = logging.getLogger(__name__)


async def create_user(
    username: str,
    email: str,
    password: str,
    role: str = "user",
    additional_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a new user.

    Args:
        username: Username
        email: Email address
        password: Password
        role: User role
        additional_data: Additional user data

    Returns:
        Created user data

    Raises:
        AuthenticationError: If there's an error creating the user
    """
    # This would typically involve a database operation
    # For now, we'll use a mock implementation

    hashed_password = authentication_service.get_password_hash(password)

    user_data = UserInDB(
        id=f"user-{username}-{datetime.now(timezone.utc).timestamp()}",
        username=username,
        email=email,
        role=role,
        hashed_password=hashed_password,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        is_active=True,
    )

    user_response = UserResponse(
        id=user_data.id,
        username=user_data.username,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active,
        created_at=user_data.created_at,
        updated_at=user_data.updated_at,
        additional_data=additional_data,
    )

    return user_response.model_dump()


async def get_user(user_id: str) -> dict[str, Any]:
    """
    Get user details by ID.

    Args:
        user_id: User ID

    Returns:
        User details

    Raises:
        NotFoundError: If the user is not found
    """
    # This would typically involve a database lookup
    # For now, we'll use a mock implementation

    if user_id == "admin-user-id":
        user_data = UserInDB(
            id=user_id,
            username="admin",
            email="admin@example.com",
            role="admin",
            hashed_password="hashed_password",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            is_active=True,
        )

        user_response = UserResponse(
            id=user_data.id,
            username=user_data.username,
            email=user_data.email,
            role=user_data.role,
            is_active=user_data.is_active,
            created_at=user_data.created_at,
            updated_at=user_data.updated_at,
        )

        return user_response.model_dump()

    logger.warning(f"User not found: {user_id}")
    raise NotFoundError(f"User with ID {user_id} not found")


async def update_user(
    user_id: str,
    update_data: UserUpdate,
) -> dict[str, Any]:
    """
    Update user details.

    Args:
        user_id: User ID
        update_data: Data to update

    Returns:
        Updated user data

    Raises:
        NotFoundError: If the user is not found
        AuthenticationError: If there's an error updating the user
    """
    # This would typically involve a database update
    # For now, we'll use a mock implementation

    if user_id != "admin-user-id":
        logger.warning(f"User not found: {user_id}")
        raise NotFoundError(f"User with ID {user_id} not found")

    user_data = UserInDB(
        id=user_id,
        username=update_data.username or "admin",
        email=update_data.email or "admin@example.com",
        role=update_data.role or "admin",
        hashed_password="hashed_password",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        is_active=update_data.is_active if update_data.is_active is not None else True,
    )

    user_response = UserResponse(
        id=user_data.id,
        username=user_data.username,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active,
        created_at=user_data.created_at,
        updated_at=user_data.updated_at,
        additional_data=update_data.additional_data,
    )

    return user_response.model_dump()


async def list_users(
    page: int = 1,
    limit: int = 10,
    role_filter: str | None = None,
) -> dict[str, Any]:
    """
    List users with pagination and filtering.

    Args:
        page: Page number
        limit: Items per page
        role_filter: Filter by role

    Returns:
        List of users and pagination information
    """
    # This would typically involve a database query
    # For now, we'll use a mock implementation

    users = [
        UserResponse(
            id="admin-user-id",
            username="admin",
            email="admin@example.com",
            role="admin",
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        UserResponse(
            id="user-1",
            username="user1",
            email="user1@example.com",
            role="user",
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        UserResponse(
            id="user-2",
            username="user2",
            email="user2@example.com",
            role="user",
            is_active=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
    ]

    if role_filter:
        users = [user for user in users if user.role == role_filter]

    total = len(users)
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    # Apply pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_users = users[start_idx:end_idx]

    pagination = PaginationInfo(
        page=page, limit=limit, total=total, total_pages=total_pages
    )

    response = {
        "items": [user.model_dump() for user in paginated_users],
        "pagination": pagination.model_dump(),
    }

    return response
