"""discover a fund family and pull its largest N-PORT positions"""

import itertools
from decimal import Decimal

from py3spread import Client

SEARCH = "vanguard"

with Client() as client:
    entities = client.fund_portfolios.entities(search=SEARCH, limit=5)["data"]
    if not entities:
        print(f"no registrants matching {SEARCH!r}")
        raise SystemExit

    print(f"registrants matching {SEARCH!r}:")
    for e in entities:
        print(f"  cik {e['cik']:<10} {e['company_name']} ({e['filing_count']} filings)")

    registrant = entities[0]
    holdings = list(itertools.islice(
        client.fund_portfolios.iter_holdings(
            registrant_cik=registrant["cik"],
            sort="val_usd",
            order="desc",
        ),
        15,
    ))

    print(f"\nlargest positions reported by {registrant['company_name']}:")
    for h in holdings:
        value = Decimal(h["val_usd"])
        pct = Decimal(h["pct_val"]) if h.get("pct_val") else None
        pct_str = f" ({pct:.2f}% of fund)" if pct is not None else ""
        print(f"  {h['name']:<45} ${value/10**6:,.1f}M{pct_str} [{h['series_name'] or h['series_id']}]")
