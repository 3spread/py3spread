"""recent 13D and 13G filings for a ticker, and who actually filed them

schedule 13D signals activist intent, 13G is passive. ticker-filtered
rows are indexed under the issuer, so the stakeholders themselves come
from each filing's reporting persons.
"""

import itertools

from py3spread import Client

TICKER = "AAPL"

with Client() as client:
    filings = list(itertools.islice(client.beneficial_ownership.iter(ticker=TICKER), 10))
    if not filings:
        print(f"no 13D/13G filings for {TICKER}")
        raise SystemExit

    print(f"recent beneficial ownership filings for {TICKER}:")
    for f in filings:
        kind = f.get("schedule_type") or f["form_type"]
        amended = " (amendment)" if f["is_amendment"] else ""
        event = f" event {f['event_date']}" if f.get("event_date") else ""
        print(f"  {f['accepted_time'][:10]}  {kind:<6}{event}{amended}")

    detail = client.beneficial_ownership.get(filings[0]["filing_id"])
    print(f"\nlatest filing: {detail['filing_id']}")
    for p in detail.get("reporting_persons") or []:
        pct = p.get("percent_of_class")
        pct = f"{float(pct):.1f}% of class" if pct else "pct not stated"
        print(f"  {p['names']}  ({pct}, source of funds {p.get('source_of_funds') or '?'})")
    print(f"source: {detail['source_url']}")
