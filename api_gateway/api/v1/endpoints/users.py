import logging

from fastapi import APIRouter, Query, status

from schemas.authentication_schema import UserCreate, UserResponse, UserUpdate
from schemas.common_schema import PaginatedResponse
from services import user_service
from shared.utils.request_handler import process_async_request

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/",
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_description="User created successfully",
    response_model=UserResponse,
)
async def create_user(user_data: UserCreate):
    async def request_handler():
        return await user_service.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role,
            additional_data=user_data.additional_data,
        )

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_201_CREATED,
        error_message="Failed to create user",
    )


@router.get(
    "/{user_id}",
    summary="Get user details",
    status_code=status.HTTP_200_OK,
    response_description="User details",
    response_model=UserResponse,
)
async def get_user(user_id: str):
    async def request_handler():
        return await user_service.get_user(user_id=user_id)

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message=f"Failed to retrieve user with ID {user_id}",
    )


@router.put(
    "/{user_id}",
    summary="Update user details",
    status_code=status.HTTP_200_OK,
    response_description="User updated successfully",
    response_model=UserResponse,
)
async def update_user(user_id: str, user_data: UserUpdate):
    async def request_handler():
        return await user_service.update_user(user_id=user_id, update_data=user_data)

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message=f"Failed to update user with ID {user_id}",
    )


@router.get(
    "/",
    summary="List users",
    status_code=status.HTTP_200_OK,
    response_description="List of users",
    response_model=PaginatedResponse[UserResponse],
)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    role_filter: str | None = Query(None, description="Filter by role"),
):
    async def request_handler():
        return await user_service.list_users(
            page=page, limit=limit, role_filter=role_filter
        )

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message="Failed to list users",
    )
