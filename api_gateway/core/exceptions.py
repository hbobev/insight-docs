import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from httpx import RequestError, TimeoutException

from shared.exceptions import (
    ApplicationError,
    AuthenticationError,
    AuthorizationError,
    DataProcessingError,
    NotFoundError,
    ServiceTimeoutError,
    ServiceUnavailableError,
    ValidationError,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register custom exception handlers with the FastAPI app.

    Args:
        app: The FastAPI application
    """

    @app.exception_handler(ApplicationError)
    async def application_error_handler(
        request: Request, exc: ApplicationError
    ) -> JSONResponse:
        """
        Handle ApplicationError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.error(f"Application error: {exc.code} - {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": exc.code,
                "detail": exc.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        """
        Handle ValidationError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.warning(f"Validation error: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": exc.code,
                "detail": exc.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(
        request: Request, exc: NotFoundError
    ) -> JSONResponse:
        """
        Handle NotFoundError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.info(f"Resource not found: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": exc.code,
                "detail": exc.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(
        request: Request, exc: AuthenticationError
    ) -> JSONResponse:
        """
        Handle AuthenticationError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.warning(f"Authentication error: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": exc.code,
                "detail": exc.message,
                "path": request.url.path,
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(AuthorizationError)
    async def authorization_error_handler(
        request: Request, exc: AuthorizationError
    ) -> JSONResponse:
        """
        Handle AuthorizationError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.warning(f"Authorization error: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": exc.code,
                "detail": exc.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(ServiceUnavailableError)
    async def service_unavailable_handler(
        request: Request, exc: ServiceUnavailableError
    ) -> JSONResponse:
        """
        Handle ServiceUnavailableError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.error(f"Service unavailable: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": exc.code,
                "detail": exc.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(ServiceTimeoutError)
    async def service_timeout_handler(
        request: Request, exc: ServiceTimeoutError
    ) -> JSONResponse:
        """
        Handle ServiceTimeoutError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.error(f"Service timeout: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={
                "error": exc.code,
                "detail": exc.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(DataProcessingError)
    async def data_processing_error_handler(
        request: Request, exc: DataProcessingError
    ) -> JSONResponse:
        """
        Handle DataProcessingError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.error(f"Data processing error: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": exc.code,
                "detail": exc.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(RequestError)
    async def http_request_error_handler(
        request: Request, exc: RequestError
    ) -> JSONResponse:
        """
        Handle HTTPX RequestError exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.error(f"HTTP request error: {str(exc)}")
        service_error = ServiceUnavailableError(
            service_name="Unknown Service",
            detail=f"Failed to communicate with a dependent service: {str(exc)}",
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": service_error.code,
                "detail": service_error.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(TimeoutException)
    async def timeout_error_handler(
        request: Request, exc: TimeoutException
    ) -> JSONResponse:
        """
        Handle HTTPX TimeoutException exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.error(f"Request timeout: {str(exc)}")
        service_error = ServiceTimeoutError(
            service_name="Unknown Service",
            detail=f"The request to a dependent service timed out: {str(exc)}",
        )
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={
                "error": service_error.code,
                "detail": service_error.message,
                "path": request.url.path,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """
        General exception handler for unhandled exceptions.

        Args:
            request: The request that caused the exception
            exc: The exception

        Returns:
            JSONResponse: A JSON response with error details
        """
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "detail": "An unexpected error occurred",
                "path": request.url.path,
            },
        )
