"""large Form D raises accepted in the last month"""

import datetime as dt
import itertools
from decimal import Decimal

from py3spread import Client

MIN_RAISE = 50_000_000

end = dt.date.today()
start = end - dt.timedelta(days=30)

with Client() as client:
    offerings = list(itertools.islice(
        client.private_offerings.iter(
            accepted_start=str(start),
            accepted_end=str(end),
            min_offering_amount=MIN_RAISE,
        ),
        25,
    ))

    print(f"form D offerings >= ${MIN_RAISE:,} accepted since {start}: {len(offerings)}")
    for o in offerings:
        print(f"  {o['accepted_time']}  {o['filer_name']}")

    if offerings:
        detail = client.private_offerings.get(offerings[0]["filing_id"])
        offering = detail.get("offering_data") or {}
        total = offering.get("total_offering_amount")
        if total:
            print(f"\nlargest recent: {detail['filer_name']}, ${Decimal(total):,.0f} offered")
        print(f"source: {detail['source_url']}")
