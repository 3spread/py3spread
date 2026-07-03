"""check what data 3spread has before querying

the platform is in public beta, so verify coverage instead of
assuming a gap is a bug.
"""

from py3spread import Client

TICKER = "AAPL"

with Client() as client:
    # per-family freshness: how recent is the newest processed filing
    asof = client.coverage.data_as_of()
    print("data freshness by family:")
    for family, info in sorted(asof["families"].items()):
        print(f"  {family:<25} {info.get('accepted_time_max')}")

    # what exists for one issuer
    cov = client.coverage.by_issuer(TICKER)
    print(f"\ncoverage for {cov['company_name']} (cik {cov['cik']}):")
    for family, info in sorted(cov["families"].items()):
        if isinstance(info, dict) and info.get("filing_count"):
            print(f"  {family:<25} {info['filing_count']} filings")

    # health also carries freshness, cheap enough to poll
    health = client.health()
    print(f"\nservice: {health['status']}")
