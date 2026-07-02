import httpx
import pytest

import py3spread
from py3spread import APIConnectionError, Client, RateLimitError
from py3spread.client import ENV_API_KEY


def test_api_key_header_and_user_agent(make_client):
    seen = {}

    def handler(request):
        seen["apikey"] = request.headers.get("apikey")
        seen["ua"] = request.headers.get("user-agent")
        return httpx.Response(200, json={"ok": True})

    client = make_client(handler)
    assert client.request("/v1/health") == {"ok": True}
    assert seen["apikey"] == "test-key"
    assert seen["ua"] == f"py3spread/{py3spread.__version__}"


def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv(ENV_API_KEY, "env-key")

    def handler(request):
        assert request.headers["apikey"] == "env-key"
        return httpx.Response(200, json={})

    client = Client(transport=httpx.MockTransport(handler))
    client.request("/v1/health")


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    with pytest.raises(ValueError):
        Client()


def test_none_params_dropped_and_ticker_upcased(make_client):
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        return httpx.Response(200, json={})

    client = make_client(handler)
    client.filings.list(ticker="aapl", form_type=None, is_valid=True)
    assert "ticker=AAPL" in seen["url"]
    assert "form_type" not in seen["url"]
    assert "is_valid=true" in seen["url"]


def test_retry_on_429_then_success(make_client):
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, json={"message": "slow down"}, headers={"retry-after": "0"})
        return httpx.Response(200, json={"ok": True})

    client = make_client(handler)
    assert client.request("/v1/health") == {"ok": True}
    assert calls["n"] == 2


def test_429_raises_after_retries_exhausted(make_client):
    def handler(request):
        return httpx.Response(429, json={"message": "API rate limit exceeded"}, headers={"retry-after": "0"})

    client = make_client(handler, max_retries=1)
    with pytest.raises(RateLimitError) as exc_info:
        client.request("/v1/health")
    assert exc_info.value.status_code == 429


def test_connection_error_wrapped(make_client):
    def handler(request):
        raise httpx.ConnectError("boom")

    client = make_client(handler, max_retries=0)
    with pytest.raises(APIConnectionError):
        client.request("/v1/health")


def test_context_manager(make_client):
    def handler(request):
        return httpx.Response(200, json={})

    with make_client(handler) as client:
        client.request("/v1/health")
