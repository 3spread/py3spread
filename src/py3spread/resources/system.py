from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

FAMILIES = (
    "insiders",
    "institutional_holdings",
    "private_offerings",
    "fund_portfolios",
    "beneficial_ownership",
    "proposed_sales",
    "fund_census",
    "money_market_funds",
    "proxy_votes",
    "reg_a_offerings",
    "registration_statements",
)


class Entities(Resource):
    """Master CIK directory."""

    def get(self, cik: str) -> dict[str, Any]:
        """Registry metadata for one CIK (person or company)."""
        return self._get(f"/v1/entities/{cik}")


class Coverage(Resource):
    """What does 3spread know, and how fresh is it."""

    def by_issuer(self, cik_or_ticker: str) -> dict[str, Any]:
        """Per-family coverage matrix for a single issuer."""
        return self._get(f"/v1/coverage/by-issuer/{cik_or_ticker}")

    def by_family(self) -> dict[str, Any]:
        """Global per-family coverage aggregates."""
        return self._get("/v1/coverage/by-family")

    def intake(self, *, period: str | None = None, lookback_days: int | None = None) -> dict[str, Any]:
        """Filing intake histogram."""
        return self._get("/v1/intake", dict(period=period, lookback_days=lookback_days))

    def data_as_of(self) -> dict[str, Any]:
        """Per-family freshness snapshot."""
        return self._get("/v1/data-as-of")


class Changes(Resource):
    """Per-family changefeed over accepted_time."""

    def list(
        self,
        family: str,
        *,
        since: str | None = None,
        until: str | None = None,
        limit: int | None = None,
        order: str | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of change events for a family (see FAMILIES)."""
        return self._get(
            f"/v1/changes/{family}",
            dict(since=since, until=until, limit=limit, order=order, cursor=cursor),
        )

    def iter(self, family: str, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate change events across pages. Same filters as list()."""
        return self._iter_cursor(f"/v1/changes/{family}", filters)
