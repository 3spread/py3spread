from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/proposed-sales"


class ProposedSales(Resource):
    """Form 144: notices of proposed sale under Rule 144."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        issuer_cik: str | None = None,
        seller_name: str | None = None,
        broker_name: str | None = None,
        securities_class_title: str | None = None,
        min_aggregate_market_value: float | str | None = None,
        max_aggregate_market_value: float | str | None = None,
        min_units_sold: float | str | None = None,
        max_units_sold: float | str | None = None,
        nothing_to_report_past_3_months: bool | None = None,
        approx_sale_start: str | None = None,
        approx_sale_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of Form 144 filings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                issuer_cik=issuer_cik,
                seller_name=seller_name,
                broker_name=broker_name,
                securities_class_title=securities_class_title,
                min_aggregate_market_value=min_aggregate_market_value,
                max_aggregate_market_value=max_aggregate_market_value,
                min_units_sold=min_units_sold,
                max_units_sold=max_units_sold,
                nothing_to_report_past_3_months=nothing_to_report_past_3_months,
                approx_sale_start=approx_sale_start,
                approx_sale_end=approx_sale_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate Form 144 filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str) -> dict[str, Any]:
        """Full detail for one Form 144 filing."""
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
