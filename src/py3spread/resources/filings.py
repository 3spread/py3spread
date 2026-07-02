from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/filings"


class Filings(Resource):
    """Cross-cutting master filings index."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        form_type: str | None = None,
        sic: str | None = None,
        is_valid: bool | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of the filings index. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                form_type=form_type,
                sic=sic,
                is_valid=is_valid,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)
