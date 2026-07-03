# py3spread

Python client for the [3spread](https://3spread.com) API: machine-readable
SEC filing data. Insider transactions, 13F holdings, fund portfolios,
beneficial ownership, private offerings, and more, normalized so the same
data point has the same key for every filer.

API keys are always free for individuals: sign up at
[3spread.com/auth/signup](https://3spread.com/auth/signup).

## Install

```bash
pip install py3spread
```

Requires Python 3.10+. One dependency (`httpx`), fully type-hinted.

## Sixty seconds

```python
from py3spread import Client

client = Client()  # reads THREESPREAD_API_KEY from the environment

# one page
page = client.filings.list(ticker="AAPL", limit=5)

# or let the client walk the pagination for you
for txn in client.insiders.iter_transactions(
    issuer_ticker="AAPL",
    transaction_start="2026-01-01",
    transaction_end="2026-06-30",
):
    print(txn["filer_name"], txn["transaction_shares"], txn["transaction_price_per_share"])
```

![manager similarity heatmap](https://raw.githubusercontent.com/3spread/py3spread/main/examples/assets/manager_similarity.png)

That heatmap is 40 lines against this client; it lives in the
[13F notebook](https://github.com/3spread/py3spread/blob/main/examples/notebooks/institutional_13f.ipynb)
along with sixteen other executed notebooks; see [Examples](examples.md).

## Where things are

- **Guides**: [authentication](guides/authentication.md),
  [pagination](guides/pagination.md), [errors](guides/errors.md),
  [data conventions](guides/data-conventions.md), and
  [keeping a store in sync](guides/sync.md)
- **Reference**: every [client](reference/client.md) method,
  [resource](reference/resources.md), and
  [exception](reference/exceptions.md), generated from the code
- **Examples**: [17 executed notebooks and 12 scripts](examples.md) on GitHub
- **Field-level semantics**: what each response field means is documented on
  the [3spread API reference](https://3spread.com/docs); this site documents
  the client

## Beta status

3spread is in [public beta](https://3spread.com/beta). History currently
reaches back to filings accepted in early 2021 and expands per the
[roadmap](https://3spread.com/roadmap). Check what is populated with
`client.coverage` before assuming a gap.
