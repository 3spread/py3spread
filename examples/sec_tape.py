"""live tape of SEC filings as 3spread ingests them

polls the changefeed for a few high-volume families and prints each new
filing once. runs until interrupted.
"""

import datetime as dt
import functools
import time

from py3spread import Client

print = functools.partial(print, flush=True)  # so the tape works piped or redirected

FAMILIES = ["insiders", "proposed_sales", "private_offerings", "beneficial_ownership"]
POLL_SECONDS = 120
LOOKBACK_DAYS = 3  # ingestion can land filings accepted a few days back

client = Client()
seen = set()
since = str(dt.date.today() - dt.timedelta(days=LOOKBACK_DAYS))

print(f"watching {', '.join(FAMILIES)} (poll every {POLL_SECONDS}s, ctrl-c to stop)")
first_pass = True
while True:
    fresh = 0
    for family in FAMILIES:
        for event in client.changes.iter(family, since=since, order="desc"):
            # forms are indexed under multiple ciks, so dedupe by accession
            accession = event["filing_id"].split("_", 1)[1]
            if accession in seen:
                continue
            seen.add(accession)
            fresh += 1
            if not first_pass:
                stamp = time.strftime("%H:%M:%S")
                print(f"{stamp}  {family:<22} form {event.get('form_type') or '?':<6}"
                      f" cik {event['cik']:<10} {event['action']}")
    if first_pass:
        print(f"baseline loaded: {len(seen)} filings in the last {LOOKBACK_DAYS} days; now tailing...")
        first_pass = False
    elif fresh:
        print(f"          ({fresh} new this poll)")
    time.sleep(POLL_SECONDS)
