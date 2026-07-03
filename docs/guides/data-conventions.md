# Data conventions

Habits that keep analyses correct. The field-level meaning of every
response is documented on the
[3spread API reference](https://3spread.com/docs); these are the
cross-cutting rules.

## Decimals are strings

Monetary and ratio fields arrive as strings at full database precision,
for example `"360836000000.00"`. Parse with `decimal.Decimal` for anything
where exactness matters; floats are fine for plotting and exploration.

```python
from decimal import Decimal

value = Decimal(holding["value_usd"])
```

## Dates and datetimes

Dates are ISO `YYYY-MM-DD`. Filing datetimes such as `accepted_time` are
timezone-naive ISO 8601 strings, currently date-granular, exactly as
processed from the SEC.

Two different time axes matter:

- `accepted_*` filters ask "what filings exist in the database": use them
  for existence and sync.
- `period_*` filters ask "what period does the filing report on": a filing
  accepted today can reference a much older period via amendments.

## Identifiers

- CIKs are accepted padded or unpadded and returned unpadded.
- Tickers must be uppercase; the client upcases for you before sending.
- `filing_id` is an opaque `{cik}_{accession}` composite. The accession
  number and `source_url` on every row link straight back to EDGAR.

## Filings can appear under more than one CIK

Forms with two parties (insider Forms 3/4/5, Schedules 13D/G) are indexed
under both the issuer's and the other party's CIK, so cross-cutting
streams can return the same accession twice. When counting or aggregating,
dedupe on the accession:

```python
accession = row["filing_id"].split("_", 1)[1]
```

The [activist radar notebook](https://github.com/3spread/py3spread/blob/main/examples/notebooks/activist_radar.ipynb)
shows the pattern in context.

## Trust the coverage endpoints

The platform is in public beta and says so. Before treating an empty
result as a bug or a signal, check what is actually populated:

```python
client.coverage.by_issuer("AAPL")   # per-family coverage for one issuer
client.coverage.data_as_of()        # per-family freshness
client.coverage.intake()            # ingestion histogram over time
```

The examples make a habit of this, and it is worth copying.
