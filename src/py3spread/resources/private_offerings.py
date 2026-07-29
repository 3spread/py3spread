from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/private-offerings"


class PrivateOfferings(Resource):
    """Form D: Regulation D exempt offering notices."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        is_amendment: bool | None = None,
        industry_group_type: str | None = None,
        investment_fund_type: str | None = None,
        min_offering_amount: float | str | None = None,
        max_offering_amount: float | str | None = None,
        min_amount_sold: float | str | None = None,
        max_amount_sold: float | str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of Form D filings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                is_amendment=is_amendment,
                industry_group_type=industry_group_type,
                investment_fund_type=investment_fund_type,
                min_offering_amount=min_offering_amount,
                max_offering_amount=max_offering_amount,
                min_amount_sold=min_amount_sold,
                max_amount_sold=max_amount_sold,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                period_start=period_start,
                period_end=period_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate Form D filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str, *, include_form_data: bool | None = None) -> dict[str, Any]:
        """Full detail for one Form D filing."""
        return self._get(f"{PATH}/{filing_id}", dict(include_form_data=include_form_data))

    def entities(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """Filer rollup. Accepts limit, offset, search, sort, order."""
        return self._entities(
            f"{PATH}/entities",
            limit=limit,
            offset=offset,
            search=search,
            sort=sort,
            order=order,
        )
