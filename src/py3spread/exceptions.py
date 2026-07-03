from __future__ import annotations

from typing import Any


class ThreeSpreadError(Exception):
    """Base class for all py3spread errors."""


class APIConnectionError(ThreeSpreadError):
    """Could not reach the API (network failure, timeout, etc.)."""


class APIError(ThreeSpreadError):
    """An HTTP error response from the API."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        code: str | None = None,
        request_id: str | None = None,
        details: Any = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.request_id = request_id
        self.details = details

    def __str__(self) -> str:
        parts = [f"{self.status_code}"]
        if self.code:
            parts.append(self.code)
        parts.append(self.message)
        if self.request_id:
            parts.append(f"(request_id: {self.request_id})")
        return " ".join(parts)


class AuthenticationError(APIError):
    """401: missing or invalid API key."""


class RateLimitError(APIError):
    """429: rate limit exceeded for your API key."""


class BadRequestError(APIError):
    """400: bad request."""


class MissingParameterError(BadRequestError):
    """400 MISSING_PARAMETER: a required filter is missing."""


class WindowTooWideError(BadRequestError):
    """400 WINDOW_TOO_WIDE: date window exceeds the endpoint maximum."""


class NotFoundError(APIError):
    """404: the requested filing, entity, or section does not exist."""


class ValidationError(APIError):
    """422: a query or path parameter failed validation."""


class ServerError(APIError):
    """500/502: server-side failure."""


class ServiceUnavailableError(ServerError):
    """503: database or query timeout, retry with backoff."""


def error_from_response(status_code: int, body: Any, headers: Any) -> APIError:
    """Map an error response to the right exception class.

    Application errors (400-503) use the {"error": {...}} envelope.
    401 and 429 come from the gateway with a plain {"message": ...} shape.
    """
    code = None
    request_id = headers.get("x-request-id") if headers else None
    details = None
    message = ""
    if isinstance(body, dict):
        err = body.get("error")
        if isinstance(err, dict):
            code = err.get("code")
            message = err.get("message") or ""
            request_id = err.get("request_id") or request_id
            details = err.get("details")
        else:
            message = body.get("message") or ""
    if not message:
        message = f"HTTP {status_code}"

    if status_code == 401:
        cls: type[APIError] = AuthenticationError
    elif status_code == 429:
        cls = RateLimitError
    elif status_code == 404:
        cls = NotFoundError
    elif status_code == 422:
        cls = ValidationError
    elif status_code == 400:
        if code == "WINDOW_TOO_WIDE":
            cls = WindowTooWideError
        elif code == "MISSING_PARAMETER":
            cls = MissingParameterError
        else:
            cls = BadRequestError
    elif status_code == 503:
        cls = ServiceUnavailableError
    elif status_code >= 500:
        cls = ServerError
    else:
        cls = APIError

    return cls(
        message,
        status_code=status_code,
        code=code,
        request_id=request_id,
        details=details,
    )
