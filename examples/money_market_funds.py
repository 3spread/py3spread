"""NAV time series for a money market fund"""

from decimal import Decimal

from py3spread import Client

SEARCH = "fidelity"

with Client() as client:
    entities = client.money_market_funds.entities(search=SEARCH, limit=1)["data"]
    if not entities:
        print(f"no registrants matching {SEARCH!r}")
        raise SystemExit
    registrant = entities[0]
    print(f"{registrant['company_name']} (cik {registrant['cik']})")

    nav = client.money_market_funds.series_nav(
        registrant_cik=registrant["cik"], order="desc", limit=12
    )["data"]
    print("\nrecent NAV per share:")
    for row in nav:
        series = row["series_name"] or row["series_id"]
        print(f"  {row['date']}  {Decimal(row['value']):.4f}  [{series}, {row['granularity']}]")

    liquid = client.money_market_funds.liquid_assets(
        registrant_cik=registrant["cik"], order="desc", limit=4
    )["data"]
    if liquid:
        print("\nrecent weekly liquid assets:")
        for row in liquid:
            pct = row.get("percentage_weekly_liquid_assets")
            series = row["series_name"] or row["series_id"]
            shown = f"{float(pct) * 100:.1f}% of assets" if pct else "not reported"
            print(f"  {row['date']}  {shown}  [{series}]")
