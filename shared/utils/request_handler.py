import logging
from datetime import datetime, timezone
from typing import Any, Callable

from fastapi import status
from fastapi.responses import JSONResponse, RedirectResponse

from shared.exceptions.base import ApplicationError

logger = logging.getLogger(__name__)


async def process_async_request(
    request_handler: Callable,
    success_status_code: int = status.HTTP_200_OK,
    error_message: str = "Resource not found",
    request_id: str | None = None,
) -> JSONResponse | RedirectResponse:
    """
    Process an asynchronous API request with standardized error handling.

    Args:
        request_handler: Async function containing the business logic to execute
        success_status_code: HTTP status code to return on successful execution
        error_message: Default error message for not found/failed requests
        request_id: Optional identifier for tracing this request in logs

    Returns:
        JSONResponse with appropriate status code and formatted content
    """
    log_prefix = f"[Request: {request_id}] " if request_id else ""

    try:
        response = await request_handler()

        if isinstance(response, RedirectResponse):
            return response

        if response is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": {"error": error_message}},
            )

        formatted_response = _format_response(response)
        return JSONResponse(status_code=success_status_code, content=formatted_response)

    except ApplicationError as ex:
        logger.error(f"{log_prefix}Application error: {str(ex)}")
        return JSONResponse(
            status_code=ex.status_code,
            content={"detail": {"error": ex.message, "code": ex.code}},
        )
    except TypeError as ex:
        # Handle type errors (often due to None values or wrong types)
        logger.error(f"{log_prefix}Type error: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": {"error": error_message, "message": str(ex)}},
        )
    except SyntaxError as ex:
        # Handle syntax errors (often from parsing operations)
        logger.error(f"{log_prefix}Syntax error in persistence layer: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": {"error": "Invalid format", "message": str(ex)}},
        )
    except ValueError as ex:
        # Handle value errors (invalid parameters)
        logger.error(f"{log_prefix}Value error: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": {"error": "Invalid value", "message": str(ex)}},
        )


def _format_response(response: Any, include_metadata: bool = True) -> dict[str, Any]:
    """
    Format API responses in a consistent structure.

    Args:
        response: The data to format (can be a Pydantic model, dict, list, or primitive)
        include_metadata: Whether to include metadata in the response

    Returns:
        A formatted response dictionary
    """
    formatted_response: dict = {}

    if response is None:
        formatted_response["data"] = None
    elif hasattr(response, "model_dump"):
        formatted_response["data"] = response.model_dump()
    elif hasattr(response, "dict"):
        formatted_response["data"] = response.dict()
    elif isinstance(response, dict):
        formatted_response["data"] = response
    elif isinstance(response, list):
        # If list contains Pydantic models, convert them
        if response and hasattr(response[0], "model_dump"):
            formatted_response["data"] = [item.model_dump() for item in response]
        elif response and hasattr(response[0], "dict"):
            formatted_response["data"] = [item.dict() for item in response]
        else:
            formatted_response["data"] = response
    elif isinstance(response, (str, int, float, bool)):
        formatted_response["data"] = {"value": response}
    else:
        # For any other types, try to convert to dict or use str representation
        try:
            formatted_response["data"] = dict(response)
        except (TypeError, ValueError):
            formatted_response["data"] = {"value": str(response)}

    if include_metadata:
        formatted_response["metadata"] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0",
        }

    return formatted_response
