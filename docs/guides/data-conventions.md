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

## Financials: version, spine, and scaling

The `/financials` family has a few conventions that differ from the
filing-family endpoints.

### Version selection is required

`statements()`, `metrics()`, `ratios()`, and `factors()` all require a
`version` argument:

- `"latest"` — newest report, restatements included
- `"original"` — as first reported
- `"as_of:YYYY-MM-DD"` — newest report known on that date (for backtests,
  to avoid look-ahead bias)

```python
client.financials.metrics(ticker="AAPL", version="latest", category="total_revenue")
client.financials.metrics(ticker="AAPL", version="as_of:2024-06-01", category="total_revenue")
```

### Spine decides the grid shape

Each statement block carries a `spine` — one of `commercial_industrial`,
`interest_spread`, `investment_company`, or `insurance` — that determines
which line items the canonical grid contains. A single filer can be
`interest_spread` on the balance sheet and `commercial_industrial` on the
income statement; the spine is chosen per statement, not per company.

### Ratios are percent-scaled, factors are raw fractions

Ratio names ending in `_pct` (e.g. `roe_pct`) are percent-scaled: `27.7`
means 27.7%. Factor `value` is a raw fraction: `1.574` means 157.4%.
Some ratio and factor names overlap (e.g. `roe`) but use different
definitions (ending vs average balances, total vs interest-bearing debt).
Pick by definition, not by name.

### Derived quarters

`derived: true` marks a discrete quarter synthesized by differencing YTD
blocks. Filter it out with `derived=False` if you only want filer-reported
periods.

### Values are raw as-filed magnitudes

Metric `value` is the raw magnitude in the filing's `currency`, not
scaled to thousands or millions. Parse with `decimal.Decimal` for exact
arithmetic. A missing metric means "not reported," never zero — absent
lines produce no row.
