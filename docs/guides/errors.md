# Errors and retries

Every HTTP error becomes a typed exception from `py3spread`, all
subclasses of `ThreeSpreadError`. Each carries `status_code`, `code`,
`message`, `request_id`, and `details` where the API provides them.

| Exception | Status | Meaning |
|---|---|---|
| `AuthenticationError` | 401 | Missing or invalid API key |
| `RateLimitError` | 429 | Rate limit exceeded (retried automatically) |
| `BadRequestError` | 400 | Bad request, e.g. an unfiltered list call |
| `MissingParameterError` | 400 | A required filter is missing |
| `WindowTooWideError` | 400 | Date window exceeds the endpoint maximum |
| `NotFoundError` | 404 | Filing, entity, or section does not exist |
| `ValidationError` | 422 | A parameter failed validation; `details` lists fields |
| `ServerError` | 500/502 | Server-side failure |
| `ServiceUnavailableError` | 503 | Timeout upstream (retried automatically) |

```python
from py3spread import Client, WindowTooWideError

client = Client()
try:
    client.filings.list(accepted_start="2024-01-01", accepted_end="2024-06-01")
except WindowTooWideError as e:
    print(e.code, e.message, e.request_id)
```

Catching `BadRequestError` covers `MissingParameterError` and
`WindowTooWideError` too, since they subclass it. The missing-filter guard
returns the specific code on most endpoints but a generic one on a few, so
key broad handling on the exception class rather than `e.code`.

## Retries

429, 502, and 503 are retried with exponential backoff, honoring
`Retry-After` when the server sends it. The default is 3 attempts;
long-running pulls that can saturate the per-minute limit should raise it:

```python
client = Client(max_retries=8)
```

Connection-level failures raise `APIConnectionError` after the same retry
budget.

## request_id

Server errors include a `request_id` (also in the `X-Request-ID` response
header). Quote it when reporting an issue to 3spread support; it is the
handle their side can trace.
