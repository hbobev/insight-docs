from http import HTTPStatus


class ApplicationError(Exception):
    """
    Base exception class for all application-specific errors.
    All custom exceptions should inherit from this class.

    Attributes:
        message (str): A message describing the error
        code (str): An application-specific error code
        status_code (int): The HTTP status code to use in responses
    """

    def __init__(
        self,
        message: str = "An application error occurred",
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        self.message = message
        self.code = code or self.__class__.__name__
        self.status_code = int(status_code)
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class ValidationError(ApplicationError):
    """Exception raised when input validation fails."""

    def __init__(
        self,
        message: str = "Validation error",
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.UNPROCESSABLE_ENTITY,
    ):
        super().__init__(message, code or "VALIDATION_ERROR", status_code)


class NotFoundError(ApplicationError):
    """Exception raised when a requested resource is not found."""

    def __init__(
        self,
        resource_type: str = "Resource",
        resource_id: str | None = None,
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.NOT_FOUND,
    ):
        message = f"{resource_type} not found"
        if resource_id:
            message = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(message, code or "NOT_FOUND_ERROR", status_code)


class AuthenticationError(ApplicationError):
    """Exception raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.UNAUTHORIZED,
    ):
        super().__init__(message, code or "AUTHENTICATION_ERROR", status_code)


class AuthorizationError(ApplicationError):
    """Exception raised when a user is not authorized to perform an action."""

    def __init__(
        self,
        message: str = "Not authorized to perform this action",
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.FORBIDDEN,
    ):
        super().__init__(message, code or "AUTHORIZATION_ERROR", status_code)


class ServiceError(ApplicationError):
    """
    Exception raised when a service operation fails.
    Base class for service-specific errors.
    """

    def __init__(
        self,
        message: str = "Service operation failed",
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message, code or "SERVICE_ERROR", status_code)


class ServiceUnavailableError(ServiceError):
    """Exception raised when a service is unavailable."""

    def __init__(
        self,
        service_name: str,
        detail: str | None = None,
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.SERVICE_UNAVAILABLE,
    ):
        message = f"Service '{service_name}' is currently unavailable"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message, code or "SERVICE_UNAVAILABLE_ERROR", status_code)


class ServiceTimeoutError(ServiceError):
    """Exception raised when a service request times out."""

    def __init__(
        self,
        service_name: str,
        detail: str | None = None,
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.GATEWAY_TIMEOUT,
    ):
        message = f"Request to service '{service_name}' timed out"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message, code or "SERVICE_TIMEOUT_ERROR", status_code)


class DataProcessingError(ApplicationError):
    """Exception raised when data processing fails."""

    def __init__(
        self,
        message: str = "Data processing failed",
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message, code or "DATA_PROCESSING_ERROR", status_code)


class ConfigurationError(ApplicationError):
    """Exception raised when there's an issue with application configuration."""

    def __init__(
        self,
        message: str = "Configuration error",
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message, code or "CONFIGURATION_ERROR", status_code)


class RateLimitExceededError(ApplicationError):
    """Exception raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        code: str | None = None,
        status_code: int | HTTPStatus = HTTPStatus.TOO_MANY_REQUESTS,
    ):
        super().__init__(message, code or "RATE_LIMIT_EXCEEDED_ERROR", status_code)
