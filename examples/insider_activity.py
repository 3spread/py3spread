"""insider sentiment and the largest insider trades for a ticker"""

import datetime as dt
from decimal import Decimal

from py3spread import Client

TICKER = "AAPL"
DAYS = 180

with Client() as client:
    ratio = client.insiders.buy_sell_ratio(ticker=TICKER, window_days=90)
    print(f"{TICKER} insider activity, {ratio['since']} to {ratio['until']}:")
    print(f"  buys:  {ratio['buys_count']:>4}  ${Decimal(ratio['buys_dollars']):,.0f}")
    print(f"  sells: {ratio['sells_count']:>4}  ${Decimal(ratio['sells_dollars']):,.0f}")

    end = dt.date.today()
    start = end - dt.timedelta(days=DAYS)
    trades = {}
    for txn in client.insiders.iter_transactions(
        issuer_ticker=TICKER,
        transaction_start=str(start),
        transaction_end=str(end),
        transaction_kind="nonderiv",
    ):
        if not txn.get("transaction_total_value"):
            continue
        # the same accession is indexed under both issuer and owner cik
        accession = txn["filing_id"].split("_", 1)[1]
        trades[(accession, txn["record_index"])] = txn
    trades = list(trades.values())

    trades.sort(key=lambda t: Decimal(t["transaction_total_value"]), reverse=True)
    print(f"\nlargest trades in the last {DAYS} days:")
    for t in trades[:10]:
        action = "bought" if t["transaction_acquired_disposed_code"] == "A" else "sold"
        value = Decimal(t["transaction_total_value"])
        print(
            f"  {t['transaction_date']}  {t['filer_name']:<30} {action} "
            f"{Decimal(t['transaction_shares']):,.0f} shares (${value:,.0f})"
        )
