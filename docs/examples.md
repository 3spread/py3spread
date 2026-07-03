# Examples

Everything lives in the repo's
[`examples/`](https://github.com/3spread/py3spread/tree/main/examples)
directory: 12 runnable scripts, a live filing tape, and 17 Jupyter
notebooks committed with their executed outputs, so GitHub renders every
table and chart without you running anything.

All of it works on a free API key
([signup](https://3spread.com/auth/signup)); the notebooks additionally
need `pandas` and `matplotlib`.

## Notebooks

In rough order of complexity:

| Notebook | What it shows |
|---|---|
| [getting_started](https://github.com/3spread/py3spread/blob/main/examples/notebooks/getting_started.ipynb) | One schema for every filer, client basics, pagination, error handling |
| [insider_analysis](https://github.com/3spread/py3spread/blob/main/examples/notebooks/insider_analysis.ipynb) | A year of insider trades in pandas, top sellers, monthly volume |
| [institutional_13f](https://github.com/3spread/py3spread/blob/main/examples/notebooks/institutional_13f.ipynb) | Berkshire's portfolio, largest holders of a stock, manager similarity heatmap |
| [fund_overlap](https://github.com/3spread/py3spread/blob/main/examples/notebooks/fund_overlap.ipynb) | Portfolio overlap between two 13F managers |
| [activist_radar](https://github.com/3spread/py3spread/blob/main/examples/notebooks/activist_radar.ipynb) | Every new 13D stake across the whole market |
| [company_360](https://github.com/3spread/py3spread/blob/main/examples/notebooks/company_360.ipynb) | One issuer across every dataset |
| [insider_vs_institutions](https://github.com/3spread/py3spread/blob/main/examples/notebooks/insider_vs_institutions.ipynb) | Insider net buying vs institutional quarter-over-quarter change |
| [form4_price_chart](https://github.com/3spread/py3spread/blob/main/examples/notebooks/form4_price_chart.ipynb) | A price chart reconstructed purely from insider filing prices |
| [form_d_heatmap](https://github.com/3spread/py3spread/blob/main/examples/notebooks/form_d_heatmap.ipynb) | Private raises by industry and month |
| [whale_quarter_diff](https://github.com/3spread/py3spread/blob/main/examples/notebooks/whale_quarter_diff.ipynb) | Berkshire's position changes between quarters |
| [insider_dossier](https://github.com/3spread/py3spread/blob/main/examples/notebooks/insider_dossier.ipynb) | One insider's full cross-issuer footprint |
| [form144_follow_through](https://github.com/3spread/py3spread/blob/main/examples/notebooks/form144_follow_through.ipynb) | Announced sales (Form 144) vs executed sales (Form 4) |
| [conviction_clone](https://github.com/3spread/py3spread/blob/main/examples/notebooks/conviction_clone.ipynb) | Concentration-ranked managers and their aggregated best ideas |
| [nport_xray](https://github.com/3spread/py3spread/blob/main/examples/notebooks/nport_xray.ipynb) | Fund composition by asset class, country, and fair-value level |
| [mmf_stress](https://github.com/3spread/py3spread/blob/main/examples/notebooks/mmf_stress.ipynb) | Every money market fund vs the 50% weekly liquidity floor |
| [tenb5_tracker](https://github.com/3spread/py3spread/blob/main/examples/notebooks/tenb5_tracker.ipynb) | Insider trades under 10b5-1 plans since the 2023 rule |
| [rate_cycle](https://github.com/3spread/py3spread/blob/main/examples/notebooks/rate_cycle.ipynb) | The Fed cycle from money market yields, with pass-through regressions |

## Scripts

Terminal-friendly versions of the common tasks: quickstart, insider
activity, 13F holdings, fund portfolios, beneficial ownership, private
offerings, money market funds, coverage checks, error handling, CSV
export, a sqlite changefeed sync, and `sec_tape.py`, a live tape of
filings as they are ingested. See the
[examples README](https://github.com/3spread/py3spread/blob/main/examples/README.md)
for the full index.
