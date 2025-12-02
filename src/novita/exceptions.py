"""Custom exceptions for the Novita SDK."""

from typing import Any


class NovitaError(Exception):
    """Base exception for all Novita SDK errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize the error.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
        """
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AuthenticationError(NovitaError):
    """Raised when authentication fails (401)."""

    def __init__(self, message: str = "Authentication failed. Check your API key.") -> None:
        """Initialize authentication error."""
        super().__init__(message, status_code=401)


class BadRequestError(NovitaError):
    """Raised when the request is malformed (400)."""

    def __init__(
        self, message: str = "Bad request. Check your request parameters.", details: Any = None
    ) -> None:
        """Initialize bad request error.

        Args:
            message: Error message
            details: Additional error details from the API
        """
        super().__init__(message, status_code=400)
        self.details = details


class RateLimitError(NovitaError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(self, message: str = "Rate limit exceeded. Please retry later.") -> None:
        """Initialize rate limit error."""
        super().__init__(message, status_code=429)


class APIError(NovitaError):
    """Raised for general API errors (5xx or unexpected errors)."""

    def __init__(
        self,
        message: str = "An API error occurred.",
        status_code: int | None = None,
        response_body: Any = None,
    ) -> None:
        """Initialize API error.

        Args:
            message: Error message
            status_code: HTTP status code
            response_body: Raw response body from the API
        """
        super().__init__(message, status_code)
        self.response_body = response_body


class NotFoundError(NovitaError):
    """Raised when a resource is not found (404)."""

    def __init__(self, message: str = "Resource not found.") -> None:
        """Initialize not found error."""
        super().__init__(message, status_code=404)


class TimeoutError(NovitaError):
    """Raised when a request times out."""

    def __init__(self, message: str = "Request timed out.") -> None:
        """Initialize timeout error."""
        super().__init__(message)
