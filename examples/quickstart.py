"""list recent SEC filings for a ticker and walk a few pages"""

import itertools

from py3spread import Client

with Client() as client:
    print("api status:", client.health()["status"])

    page = client.filings.list(ticker="AAPL", limit=5)
    print(f"\nlatest {page['returned']} AAPL filings:")
    for f in page["data"]:
        print(f"  {f['accepted_time']}  form {f['form_type']:<6} {f['filer_name']}")
        print(f"    {f['source_url']}")

    # iter() pages with the cursor automatically
    forms = [f["form_type"] for f in itertools.islice(client.filings.iter(ticker="AAPL"), 50)]
    print(f"\nform types across the last {len(forms)} filings:")
    for form in sorted(set(forms)):
        print(f"  {form}: {forms.count(form)}")
