"""export a manager's latest 13F holdings to csv

values are strings at full precision in the API; Decimal keeps them exact.
"""

import csv
import itertools
from decimal import Decimal

from py3spread import Client

MANAGER_CIK = "1067983"  # berkshire hathaway
OUT = "holdings.csv"

with Client() as client:
    filings = client.institutional_holdings.list(filing_manager_cik=MANAGER_CIK, limit=1)["data"]
    if not filings:
        print(f"no 13F filings for cik {MANAGER_CIK}")
        raise SystemExit
    filing = filings[0]
    print(f"{filing['filer_name']}, period {filing['period_of_report']}")

    rows = itertools.islice(
        client.institutional_holdings.iter_holdings(filing_id=filing["filing_id"]),
        5000,
    )
    fields = ["name_of_issuer", "title_of_class", "cusip", "ssh_prnamt", "ssh_prnamt_type", "value_usd"]
    count = 0
    total = Decimal(0)
    with open(OUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            total += Decimal(row["value_usd"])
            count += 1

print(f"wrote {count} holdings (${total:,.0f} reported value) to {OUT}")
