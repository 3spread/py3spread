"""keep a local sqlite store in sync with the insiders changefeed

run it repeatedly (cron, systemd timer, a loop); each run picks up
where the last one stopped.
"""

import datetime as dt
import sqlite3

from py3spread import Client

DB = "filings_sync.db"
FAMILY = "insiders"

conn = sqlite3.connect(DB)
conn.execute(
    "create table if not exists filings ("
    " filing_id text primary key, cik text, form_type text,"
    " accepted_time text, action text)"
)
conn.execute("create table if not exists sync_state (family text primary key, since text)")

row = conn.execute("select since from sync_state where family = ?", (FAMILY,)).fetchone()
stored = row[0] if row else "2026-06-25T00:00:00"
# rewind a couple of days: filings can be processed after their accepted_time,
# landing behind a previously saved cursor; the upsert makes the overlap safe
since = (dt.datetime.fromisoformat(stored) - dt.timedelta(days=2)).isoformat()
print(f"syncing {FAMILY} since {since}")

new = 0
latest = since
with Client() as client:
    for event in client.changes.iter(FAMILY, since=since, order="asc"):
        conn.execute(
            "insert into filings values (?, ?, ?, ?, ?)"
            " on conflict(filing_id) do update set action = excluded.action,"
            " accepted_time = excluded.accepted_time",
            (
                event["filing_id"],
                event["cik"],
                event.get("form_type"),
                event["accepted_time"],
                event["action"],
            ),
        )
        latest = max(latest, event["accepted_time"])
        new += 1

conn.execute(
    "insert into sync_state values (?, ?) on conflict(family) do update set since = excluded.since",
    (FAMILY, max(latest, stored)),  # the cursor only moves forward
)
conn.commit()

total = conn.execute("select count(*) from filings").fetchone()[0]
print(f"applied {new} events (overlap included), store has {total} filings")
conn.close()
