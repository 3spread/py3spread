# Authentication

Every data endpoint needs a credential. The client takes either a long-lived
**API key** or a short-lived **OAuth access token**.

API keys are always free for individuals: sign up at
[3spread.com/auth/signup](https://3spread.com/auth/signup) and provision one
from your dashboard.

## Giving the client your key

The client reads `THREESPREAD_API_KEY` from the environment:

```bash
export THREESPREAD_API_KEY=your_key
```

```python
from py3spread import Client

client = Client()
```

Or pass it explicitly:

```python
client = Client(api_key="your_key")
```

The key is sent as the `apikey` header. The API also accepts `X-API-Key`
and `Authorization: Bearer`, but the client handles this for you.

## OAuth access tokens

If you obtained a token through an OAuth flow rather than provisioning a key,
pass it as `access_token`:

```python
client = Client(access_token="eyJ...")
```

It is sent as `Authorization: Bearer` and no `apikey` header is set. Passing
both `api_key` and `access_token` raises `ValueError` — pick one.

Unlike the API key, an access token is **never read from the environment**.
Tokens are short-lived, so one pinned into a process environment would be
expired for most of that process's life. The token is bound when the client is
constructed, so refreshing means building a new client:

```python
def client_for(token: str) -> Client:
    return Client(access_token=token)
```

Both credentials resolve to the same account and share one rate-limit budget,
so moving between them does not give you a second quota.

## Rate limits

Community keys allow 36,000 requests per hour (600 requests per minute).
The client retries 429 responses automatically with backoff; for long
pulls that may saturate the window, raise the retry budget:

```python
client = Client(max_retries=8)
```

## Rotation and failures

Rotate keys from the 3spread dashboard; rotation is immediate. A missing or
invalid key raises
[`AuthenticationError`](../reference/exceptions.md) with the server's
message attached.

Never commit a key. All the examples in this repo read the environment
variable, which is the pattern to copy.
