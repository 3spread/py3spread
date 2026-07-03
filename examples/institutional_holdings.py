"""who holds a stock per the latest 13F filings, largest positions first"""

import itertools
from decimal import Decimal

from py3spread import Client

CUSIP = "037833100"  # apple

with Client() as client:
    holdings = list(itertools.islice(
        client.institutional_holdings.iter_holdings(
            cusip=CUSIP,
            min_value=1_000_000_000,
            sort="value",
            order="desc",
        ),
        20,
    ))

    if not holdings:
        print("no holdings found")
        raise SystemExit

    print(f"largest reported positions in {holdings[0]['name_of_issuer']}:")
    for h in holdings:
        value = Decimal(h["value_usd"])
        shares = Decimal(h["ssh_prnamt"])
        print(
            f"  {h['filing_manager_name']:<45} ${value/10**9:,.1f}B "
            f"({shares:,.0f} {h['ssh_prnamt_type']}, period {h['period_of_report']})"
        )

    # drill into one manager's filing history
    manager = holdings[0]
    print(f"\nrecent 13F filings by {manager['filing_manager_name']}:")
    page = client.institutional_holdings.list(
        filing_manager_cik=manager["filing_manager_cik"], limit=5
    )
    for f in page["data"]:
        print(f"  {f['accepted_time']}  {f['form_type']}  period {f['period_of_report']}")
