# Pagination

The API uses two pagination styles. The client implements both, and the
`iter*()` methods hide the difference entirely.

## The easy way: iterators

Every list-style endpoint has an iterator variant that yields rows and
follows pages for you:

```python
for filing in client.filings.iter(ticker="AAPL"):
    ...

for holding in client.institutional_holdings.iter_holdings(cusip="037833100"):
    ...
```

Use `itertools.islice` to cap how much you pull:

```python
import itertools

first_500 = list(itertools.islice(client.filings.iter(ticker="AAPL"), 500))
```

## Under the hood

**Cursor (keyset) endpoints** (the high-volume windowed lists such as
`/filings`, `/insiders`, `/beneficial-ownership`, and the changefeed)
return `next_cursor`. The iterator resends your filters plus the cursor
until it is exhausted. Cursors never duplicate a boundary row.

**Offset endpoints** (streams like `iter_transactions` and
`iter_holdings`, plus the `entities` rollups) page with `limit`/`offset`.
The iterator advances the offset until `has_more` goes false or the total
is reached.

One wrinkle worth knowing: on cursor endpoints the `limit` field in the
response body is the endpoint's fixed page cap, not an echo of what you
sent; `returned` is the actual row count.

## Filters are required

Windowed lists refuse fully unfiltered calls. Supply at least one identity
filter (`cik`, `ticker`, or a family id like `issuer_cik`) or a fully
bounded date window. Bounded windows have per-endpoint maximum widths and
return `WindowTooWideError` beyond them; for wide ranges, filter by
identity and let the iterator walk.

A few endpoints add their own requirements (for example
`insiders.transactions` needs a `transaction_start`/`transaction_end`
window). The error messages state exactly what is missing.
