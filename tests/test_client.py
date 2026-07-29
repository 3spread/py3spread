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


def test_access_token_sent_as_bearer_and_no_apikey_header(monkeypatch):
    # The gateway picks the auth plugin by header: an OAuth token has to arrive
    # as Authorization, and a stale apikey header alongside it would be tried
    # first by key-auth and fail.
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    seen = {}

    def handler(request):
        seen["authorization"] = request.headers.get("authorization")
        seen["apikey"] = request.headers.get("apikey")
        return httpx.Response(200, json={"ok": True})

    client = Client(access_token="eyJ-token", transport=httpx.MockTransport(handler))
    assert client.request("/v1/health") == {"ok": True}
    assert seen["authorization"] == "Bearer eyJ-token"
    assert seen["apikey"] is None


def test_access_token_beats_env_api_key(monkeypatch):
    # An explicit token is a deliberate act; an ambient env key must not win.
    monkeypatch.setenv(ENV_API_KEY, "env-key")

    def handler(request):
        assert request.headers.get("authorization") == "Bearer tok"
        assert request.headers.get("apikey") is None
        return httpx.Response(200, json={})

    client = Client(access_token="tok", transport=httpx.MockTransport(handler))
    client.request("/v1/health")


def test_api_key_and_access_token_together_raises(monkeypatch):
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    with pytest.raises(ValueError, match="not both"):
        Client("sk_live_x", access_token="eyJ-token")


def test_access_token_is_not_read_from_env(monkeypatch):
    # Deliberate: OAuth tokens are short-lived, so there is no env fallback for
    # them the way there is for the long-lived API key.
    monkeypatch.delenv(ENV_API_KEY, raising=False)
    monkeypatch.setenv("THREESPREAD_ACCESS_TOKEN", "eyJ-from-env")
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
