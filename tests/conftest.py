import httpx
import pytest

from py3spread import Client


@pytest.fixture
def make_client():
    def _make(handler, **kwargs):
        return Client("test-key", transport=httpx.MockTransport(handler), **kwargs)

    return _make
