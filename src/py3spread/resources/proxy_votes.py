from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/proxy-votes"


class ProxyVotes(Resource):
    """Form N-PX: annual proxy voting record reports."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        report_type: str | None = None,
        report_calendar_year: int | None = None,
        is_amendment: bool | None = None,
        confidential_treatment: bool | None = None,
        registrant_type: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of N-PX filings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                report_type=report_type,
                report_calendar_year=report_calendar_year,
                is_amendment=is_amendment,
                confidential_treatment=confidential_treatment,
                registrant_type=registrant_type,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate N-PX filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str, *, include_form_data: bool | None = None) -> dict[str, Any]:
        """Full detail for one N-PX filing, with vote records."""
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
        """Fund rollup. Accepts limit, offset, search, sort, order."""
        return self._entities(
            f"{PATH}/entities",
            limit=limit,
            offset=offset,
            search=search,
            sort=sort,
            order=order,
        )
