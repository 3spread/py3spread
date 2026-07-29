from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/registration-statements"


class RegistrationStatements(Resource):
    """Registration statements with pre-segmented text sections."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        form_type: str | None = None,
        is_valid: bool | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """One page of registration statements (offset paged)."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                form_type=form_type,
                is_valid=is_valid,
                period_start=period_start,
                period_end=period_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                offset=offset,
                sort=sort,
                order=order,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate registration statements across pages. Same filters as list()."""
        return self._iter_offset(PATH, filters)

    def get(self, filing_id: str) -> dict[str, Any]:
        """Full detail for one registration statement."""
        return self._get(f"{PATH}/{filing_id}")

    def sections(
        self,
        *,
        filing_id: str | None = None,
        cik: str | None = None,
        ticker: str | None = None,
        form_type: str | None = None,
        section_title: str | None = None,
        min_text_length: int | None = None,
        max_text_length: int | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        include_text: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """One page of the sections stream."""
        return self._get(
            f"{PATH}/sections",
            dict(
                filing_id=filing_id,
                cik=cik,
                ticker=ticker,
                form_type=form_type,
                section_title=section_title,
                min_text_length=min_text_length,
                max_text_length=max_text_length,
                period_start=period_start,
                period_end=period_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                include_text=include_text,
                limit=limit,
                offset=offset,
                sort=sort,
                order=order,
            ),
        )

    def iter_sections(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate sections across pages. Same filters as sections()."""
        return self._iter_offset(f"{PATH}/sections", filters)

    def get_section(self, section_id: str) -> dict[str, Any]:
        """One text section by UUID."""
        return self._get(f"{PATH}/sections/{section_id}")

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
