"""financial statements, metrics, ratios, and quant factors for a ticker

The financials family covers validated 10-K / 10-Q data: canonical
statement blocks, line-item metrics, precomputed ratios, and a 90-factor
quant library.  version selection (latest / original / as_of:YYYY-MM-DD)
is required on the series endpoints.
"""

from decimal import Decimal

from py3spread import Client

TICKER = "AAPL"

with Client() as client:
    # -- filings discovery --
    page = client.financials.list(ticker=TICKER, form_type="10-K", limit=3)
    print(f"latest {page['returned']} 10-K filings for {TICKER}:")
    for f in page["data"]:
        print(
            f"  {f['period_of_report']}  {f['form_type']:<6} "
            f"{f['statement_count']} blocks  avg_score {f['avg_composite']}"
        )

    # -- statements (canonical grid per block) --
    stmts = client.financials.statements(
        ticker=TICKER, version="latest", statement_type="inc", limit=1,
    )
    if stmts["data"]:
        block = stmts["data"][0]
        print(f"\nlatest income statement block:")
        print(f"  period: {block['period_end']}  Q{block['fiscal_quarter']} FY{block['fiscal_year']}")
        print(f"  spine: {block['spine']}  score: {block['score_composite']}")
        grid = block["statement_json"]
        for section, lines in grid.get("sections", {}).items():
            print(f"  [{section}]")
            for cat, cell in lines.items():
                val = cell.get("value")
                src = cell.get("source")
                if val is not None:
                    print(f"    {cat:<40} {val:>20}  ({src})")

    # -- metrics (raw line-item time-series) --
    print(f"\n{TICKER} total revenue across recent periods:")
    for m in client.financials.iter_metrics(
        ticker=TICKER, version="latest", category="total_revenue",
        period_length=3,  # discrete quarters only
    ):
        val = Decimal(m["value"])
        print(f"  {m['period_end']}  Q{m['fiscal_quarter']} FY{m['fiscal_year']}  ${val:,.0f}")

    # -- ratios (precomputed, percent-scaled for _pct names) --
    print(f"\n{TICKER} ROE across recent periods:")
    for r in client.financials.iter_ratios(
        ticker=TICKER, version="latest", ratio_name="roe_pct",
    ):
        print(
            f"  {r['period_end']}  Q{r['fiscal_quarter']} FY{r['fiscal_year']}  "
            f"ROE {r['value']}%  (pctile {r.get('value_pctile', 'N/A')})"
        )

    # -- factors (quant library, raw fractions not percents) --
    print(f"\n{TICKER} ROE factor (raw fraction, FY):")
    for f in client.financials.iter_factors(
        ticker=TICKER, version="latest", factor_name="roe", period_type="FY",
    ):
        print(
            f"  {f['period_end']}  FY{f['fiscal_year']}  "
            f"roe {f['value']}  pctile {f.get('value_pctile', 'N/A')}"
        )

    # -- factor percentile (point-in-time rank) --
    latest_fy = list(client.financials.iter_factors(
        ticker=TICKER, version="latest", factor_name="roe", period_type="FY", limit=1,
    ))
    if latest_fy:
        pe = latest_fy[0]["period_end"]
        pct = client.financials.factor_percentile(
            ticker=TICKER, factor_name="roe", period_type="FY",
            period_end=pe, as_of="2026-09-01",
        )
        print(f"\npoint-in-time percentile (as of 2026-09-01):")
        print(f"  {pct['factor_name']} for {pe}: {pct['percentile']} pctile")
        print(f"  cohort size: {pct['cohort_size']}")

    # -- vocabularies --
    cats = client.financials.categories()
    print(f"\n{len(cats['data'])} metric categories available")

    rnames = client.financials.ratio_names()
    print(f"{len(rnames['data'])} ratio names available")

    fnames = client.financials.factor_names()
    print(f"{len(fnames['data'])} factor names available")
