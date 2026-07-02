from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/institutional-holdings"


class InstitutionalHoldings(Resource):
    """Form 13F: institutional investment manager quarterly holdings."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        filing_manager_cik: str | None = None,
        report_type: str | None = None,
        is_amendment: bool | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of 13F filings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                filing_manager_cik=filing_manager_cik,
                report_type=report_type,
                is_amendment=is_amendment,
                period_start=period_start,
                period_end=period_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate 13F filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str) -> dict[str, Any]:
        """Full detail for one 13F filing."""
        return self._get(f"{PATH}/{filing_id}")

    def holdings(
        self,
        *,
        cusip: str | None = None,
        name_of_issuer: str | None = None,
        filing_manager_cik: str | None = None,
        filing_id: str | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        period: str | None = None,
        min_value: float | str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """One page of the cross-filing holdings stream."""
        return self._get(
            f"{PATH}/holdings",
            dict(
                cusip=cusip,
                name_of_issuer=name_of_issuer,
                filing_manager_cik=filing_manager_cik,
                filing_id=filing_id,
                period_start=period_start,
                period_end=period_end,
                period=period,
                min_value=min_value,
                limit=limit,
                offset=offset,
                sort=sort,
                order=order,
            ),
        )

    def iter_holdings(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate holdings across pages. Same filters as holdings()."""
        return self._iter_offset(f"{PATH}/holdings", filters)
