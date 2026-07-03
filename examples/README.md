# py3spread examples

Runnable scripts showing common uses of the 3spread API. Each one needs an
API key in the environment:

```bash
export THREESPREAD_API_KEY=your_key
python examples/quickstart.py
```

| Script | What it shows |
|---|---|
| `quickstart.py` | Health check, listing filings, walking pages |
| `insider_activity.py` | Buy/sell sentiment and the largest insider trades for a ticker |
| `institutional_holdings.py` | Who holds a stock (13F), largest positions first |
| `fund_portfolios.py` | Discover a fund family and pull its top N-PORT positions |
| `beneficial_ownership.py` | Recent 13D/13G filers for a ticker |
| `private_offerings.py` | Large recent Form D raises |
| `money_market_funds.py` | NAV time series for a money market fund |
| `changefeed_sync.py` | Keep a local sqlite store in sync via the changefeed |
| `coverage_and_freshness.py` | Check what data exists before querying |
| `errors_and_retries.py` | Typed exceptions and what triggers them |
| `export_csv.py` | Dump 13F holdings to a CSV with correct decimal handling |

## Notebooks

Jupyter notebooks with saved outputs live in `notebooks/`. They additionally
need `pandas` and `matplotlib` (`pip install pandas matplotlib`).

In rough order of complexity:

| Notebook | What it shows |
|---|---|
| `notebooks/getting_started.ipynb` | One schema for every filer, client basics, pagination, error handling |
| `notebooks/insider_analysis.ipynb` | A year of insider trades in pandas, top sellers, monthly volume chart |
| `notebooks/institutional_13f.ipynb` | Berkshire's 13F portfolio, largest holders of a stock, manager similarity heatmap |
| `notebooks/fund_overlap.ipynb` | Portfolio overlap between two 13F managers |
| `notebooks/activist_radar.ipynb` | Every new 13D stake across the whole market, with filing anatomy |
| `notebooks/company_360.ipynb` | One issuer across every dataset: profile, coverage, insiders, owners, 13D/G, Form 144 |
| `notebooks/insider_vs_institutions.ipynb` | Cross-dataset study: insider net buying vs institutional QoQ change |
| `notebooks/form4_price_chart.ipynb` | A price chart reconstructed purely from insider filing prices |
| `notebooks/form_d_heatmap.ipynb` | Private raises by industry and month from Form D |
| `notebooks/whale_quarter_diff.ipynb` | Berkshire's position changes between quarters |
| `notebooks/insider_dossier.ipynb` | One insider's full cross-issuer footprint (Tim Cook: AAPL + NKE) |
| `notebooks/form144_follow_through.ipynb` | Announced sales (Form 144) vs executed sales (Form 4) |
| `notebooks/conviction_clone.ipynb` | Concentration-ranked managers and their aggregated best ideas |
| `notebooks/nport_xray.ipynb` | Fund composition by asset class, country, and fair-value level |
| `notebooks/mmf_stress.ipynb` | Every money market fund vs the 50% weekly liquidity floor |
| `notebooks/tenb5_tracker.ipynb` | Share of insider trades under 10b5-1 plans since the 2023 rule |
| `notebooks/rate_cycle.ipynb` | The Fed cycle reconstructed from money market yields, with pass-through regressions |

There is also `sec_tape.py`, a terminal script that tails the changefeed and
prints new filings as they are ingested.

Get a free key at [3spread.com/auth/signup](https://3spread.com/auth/signup).
