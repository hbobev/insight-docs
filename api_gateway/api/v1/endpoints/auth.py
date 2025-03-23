"""
Authentication API endpoints for the API Gateway.
"""
import logging

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer

from schemas.authentication_schema import Token, TokenRefresh, UserLogin
from services import authentication_service
from shared.utils.request_handler import process_async_request

router = APIRouter()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


@router.post(
    "/login",
    summary="Authenticate user and get access token",
    status_code=status.HTTP_200_OK,
    response_description="Access and refresh tokens",
    response_model=Token,
)
async def login(form_data: UserLogin):
    """
    Authenticate a user and get access token.

    Args:
        form_data: User login data

    Returns:
        Access and refresh tokens
    """

    async def request_handler():
        user = await authentication_service.authenticate_user(
            form_data.username, form_data.password
        )

        access_token = authentication_service.create_access_token(
            data={"sub": user["id"]}
        )
        refresh_token = authentication_service.create_refresh_token(user_id=user["id"])

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message="Authentication failed",
    )


@router.post(
    "/refresh",
    summary="Refresh access token",
    status_code=status.HTTP_200_OK,
    response_description="New access token",
    response_model=Token,
)
async def refresh_token(refresh_token_data: TokenRefresh):
    """
    Refresh an access token using a refresh token.

    Args:
        refresh_token_data: Refresh token data

    Returns:
        New access token
    """

    async def request_handler():
        token_data = authentication_service.decode_token(
            refresh_token_data.refresh_token
        )

        if token_data.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        access_token = authentication_service.create_access_token(
            data={"sub": token_data.get("sub")}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_200_OK,
        error_message="Token refresh failed",
    )


@router.post(
    "/logout",
    summary="Logout user",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="No content",
)
async def logout(response: Response):
    """
    Logout a user by invalidating their tokens.

    In a stateless JWT system, we can't truly invalidate tokens without a blacklist.
    This endpoint mainly serves to clear cookies if they're being used.

    Returns:
        No content on success
    """
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    async def request_handler():
        # In a stateless JWT system, we don't need to do anything server-side
        # In a real application, we might add the token to a blacklist
        return None

    return await process_async_request(
        request_handler=request_handler,
        success_status_code=status.HTTP_204_NO_CONTENT,
        error_message="Logout failed",
    )
