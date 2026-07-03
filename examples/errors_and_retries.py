"""what the typed exceptions look like in practice

429, 502, and 503 are retried automatically; everything else raises
immediately with status_code, code, and request_id attached.
"""

from py3spread import (
    BadRequestError,
    Client,
    NotFoundError,
    ValidationError,
    WindowTooWideError,
)

with Client() as client:
    # windowed lists need a filter
    try:
        client.filings.list()
    except BadRequestError as e:
        print(f"unfiltered call -> {type(e).__name__}: {e.message}")

    # bounded windows have per-endpoint maximums
    try:
        client.filings.list(accepted_start="2024-01-01", accepted_end="2024-06-01")
    except WindowTooWideError as e:
        print(f"wide window -> {type(e).__name__}: {e.message}")

    # parameter validation failures carry field-level details
    try:
        client.filings.list(ticker="NOT A TICKER")
    except ValidationError as e:
        print(f"bad ticker -> {type(e).__name__}: {e.details}")

    # unknown ids are a 404
    try:
        client.insiders.get("9999999_0000000000-00-000000")
    except NotFoundError as e:
        print(f"missing filing -> {type(e).__name__} (request_id {e.request_id})")
