import httpx
import pytest

from py3spread import (
    AuthenticationError,
    BadRequestError,
    MissingParameterError,
    NotFoundError,
    ServerError,
    ServiceUnavailableError,
    ValidationError,
    WindowTooWideError,
)


def _client_returning(make_client, status, body, headers=None):
    def handler(request):
        return httpx.Response(status, json=body, headers=headers or {})

    # max_retries=0 so 5xx errors surface instead of retrying
    return make_client(handler, max_retries=0)


def test_gateway_401(make_client):
    client = _client_returning(make_client, 401, {"message": "Missing API key in request"})
    with pytest.raises(AuthenticationError) as exc_info:
        client.request("/v1/filings")
    assert exc_info.value.message == "Missing API key in request"
    assert exc_info.value.code is None


def test_window_too_wide(make_client):
    body = {"error": {"code": "WINDOW_TOO_WIDE", "message": "window too wide", "request_id": "req-1"}}
    client = _client_returning(make_client, 400, body)
    with pytest.raises(WindowTooWideError) as exc_info:
        client.request("/v1/filings")
    err = exc_info.value
    assert err.code == "WINDOW_TOO_WIDE"
    assert err.request_id == "req-1"
    assert isinstance(err, BadRequestError)


def test_missing_parameter(make_client):
    body = {"error": {"code": "MISSING_PARAMETER", "message": "need a filter"}}
    client = _client_returning(make_client, 400, body)
    with pytest.raises(MissingParameterError):
        client.request("/v1/filings")


def test_not_found(make_client):
    body = {"error": {"code": "HTTP_404", "message": "not found"}}
    client = _client_returning(make_client, 404, body)
    with pytest.raises(NotFoundError):
        client.request("/v1/insiders/nope")


def test_validation_error_with_details(make_client):
    details = [{"loc": ["query", "ticker"], "msg": "bad pattern", "type": "string_pattern_mismatch"}]
    body = {"error": {"code": "VALIDATION_ERROR", "message": "validation failed", "details": details}}
    client = _client_returning(make_client, 422, body)
    with pytest.raises(ValidationError) as exc_info:
        client.request("/v1/filings")
    assert exc_info.value.details == details


def test_server_error_request_id_from_header(make_client):
    body = {"error": {"code": "INTERNAL_ERROR", "message": "oops"}}
    client = _client_returning(make_client, 500, body, headers={"x-request-id": "req-hdr"})
    with pytest.raises(ServerError) as exc_info:
        client.request("/v1/filings")
    assert exc_info.value.request_id == "req-hdr"


def test_service_unavailable(make_client):
    body = {"error": {"code": "SERVICE_UNAVAILABLE", "message": "db timeout"}}
    client = _client_returning(make_client, 503, body)
    with pytest.raises(ServiceUnavailableError):
        client.request("/v1/filings")


def test_non_json_error_body(make_client):
    def handler(request):
        return httpx.Response(500, text="Internal Server Error")

    client = make_client(handler, max_retries=0)
    with pytest.raises(ServerError) as exc_info:
        client.request("/v1/filings")
    assert "Internal Server Error" in exc_info.value.message
