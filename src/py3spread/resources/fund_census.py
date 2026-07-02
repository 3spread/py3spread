from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/fund-census"


class FundCensus(Resource):
    """Form N-CEN: annual investment company census reports."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        registrant_cik: str | None = None,
        registrant_lei: str | None = None,
        investment_company_type: str | None = None,
        is_report_period_lt_12: bool | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of N-CEN filings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                registrant_cik=registrant_cik,
                registrant_lei=registrant_lei,
                investment_company_type=investment_company_type,
                is_report_period_lt_12=is_report_period_lt_12,
                period_start=period_start,
                period_end=period_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate N-CEN filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str, *, include_form_data: bool | None = None) -> dict[str, Any]:
        """Full detail for one N-CEN filing."""
        return self._get(f"{PATH}/{filing_id}", dict(include_form_data=include_form_data))

    def entities(self, **kwargs: Any) -> dict[str, Any]:
        """Registrant rollup. Accepts limit, offset, search, sort, order."""
        return self._entities(f"{PATH}/entities", **kwargs)
