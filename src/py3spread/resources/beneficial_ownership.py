from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/beneficial-ownership"


class BeneficialOwnership(Resource):
    """Schedule 13D / 13G: 5%+ beneficial ownership reports."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        schedule_type: str | None = None,
        issuer_cusip: str | None = None,
        issuer_name: str | None = None,
        amendment_no: str | None = None,
        event_date_start: str | None = None,
        event_date_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of 13D/13G filings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                schedule_type=schedule_type,
                issuer_cusip=issuer_cusip,
                issuer_name=issuer_name,
                amendment_no=amendment_no,
                event_date_start=event_date_start,
                event_date_end=event_date_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate 13D/13G filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str) -> dict[str, Any]:
        """Full detail for one 13D/13G filing."""
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
        """Filer rollup. Accepts limit, offset, search, sort, order."""
        return self._entities(
            f"{PATH}/entities",
            limit=limit,
            offset=offset,
            search=search,
            sort=sort,
            order=order,
        )
