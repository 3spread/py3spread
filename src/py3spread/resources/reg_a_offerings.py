from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/reg-a-offerings"


class RegAOfferings(Resource):
    """Regulation A+ offerings: Forms 1-A / 1-K / 1-U / 1-Z."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        tier: str | None = None,
        audit_status: str | None = None,
        issuer_industry_group: str | None = None,
        jurisdiction_of_organization: str | None = None,
        min_aggregate_offering: float | str | None = None,
        max_aggregate_offering: float | str | None = None,
        min_total_assets: float | str | None = None,
        max_total_assets: float | str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of Reg A+ offerings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                tier=tier,
                audit_status=audit_status,
                issuer_industry_group=issuer_industry_group,
                jurisdiction_of_organization=jurisdiction_of_organization,
                min_aggregate_offering=min_aggregate_offering,
                max_aggregate_offering=max_aggregate_offering,
                min_total_assets=min_total_assets,
                max_total_assets=max_total_assets,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate Reg A+ offerings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str) -> dict[str, Any]:
        """Full detail for one Reg A+ filing."""
        return self._get(f"{PATH}/{filing_id}")

    def entities(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """Issuer rollup. Accepts limit, offset, search, sort, order."""
        return self._entities(
            f"{PATH}/entities",
            limit=limit,
            offset=offset,
            search=search,
            sort=sort,
            order=order,
        )
