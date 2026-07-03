# Syncing a downstream store

The changefeed streams per-family events ordered by acceptance time, which
makes it the intended way to keep a database in sync without re-querying
list endpoints.

```python
for event in client.changes.iter("insiders", since="2026-07-01T00:00:00", order="asc"):
    upsert(event["filing_id"], event["cik"], event["accepted_time"], event["action"])
```

Events carry `filing_id`, `cik`, `form_type`, `accepted_time`, and an
`action` of `created` or `amended`. Eleven families each have a feed; see
`py3spread.FAMILIES` for the list.

## The lookback rule

Filings can be processed a few days after their acceptance date, which
places them behind a cursor you already saved. A sync that resumes from
exactly its last position can miss them permanently. The robust pattern:

1. resume from your saved position minus a lookback margin (a few days)
2. make writes idempotent (upsert on `filing_id`)
3. only move the saved position forward

```python
since = (last_synced - timedelta(days=2)).isoformat()
```

The overlap re-applies a few thousand events per run; the upserts make
that free. A complete worked example with sqlite state lives in
[`examples/changefeed_sync.py`](https://github.com/3spread/py3spread/blob/main/examples/changefeed_sync.py),
and a live terminal tape in
[`examples/sec_tape.py`](https://github.com/3spread/py3spread/blob/main/examples/sec_tape.py).

## Freshness checks

`client.health()` returns `data_as_of` per family in one cheap call, which
is the right probe for "has anything new landed" before a heavier sync
pass. `client.coverage.data_as_of()` gives the same per-family snapshot
with more detail.
