# Authentication

Every data endpoint needs an API key. Keys are always free for individuals:
sign up at [3spread.com/auth/signup](https://3spread.com/auth/signup) and
provision one from your dashboard.

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
