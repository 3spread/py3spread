from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/fund-portfolios"


class FundPortfolios(Resource):
    """Form N-PORT: registered investment company monthly portfolio holdings."""

    def list(
        self,
        *,
        registrant_cik: str | None = None,
        series_id: str | None = None,
        class_id: str | None = None,
        is_confidential: bool | None = None,
        is_final_filing: bool | None = None,
        report_period_start: str | None = None,
        report_period_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """One page of N-PORT filings (offset paged)."""
        return self._get(
            PATH,
            dict(
                registrant_cik=registrant_cik,
                series_id=series_id,
                class_id=class_id,
                is_confidential=is_confidential,
                is_final_filing=is_final_filing,
                report_period_start=report_period_start,
                report_period_end=report_period_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                offset=offset,
                sort=sort,
                order=order,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate N-PORT filings across pages. Same filters as list()."""
        return self._iter_offset(PATH, filters)

    def get(self, filing_id: str, *, include_form_data: bool | None = None) -> dict[str, Any]:
        """Full detail for one N-PORT filing."""
        return self._get(f"{PATH}/{filing_id}", dict(include_form_data=include_form_data))

    def holdings(
        self,
        *,
        cusip: str | None = None,
        isin: str | None = None,
        lei: str | None = None,
        name: str | None = None,
        registrant_cik: str | None = None,
        filing_id: str | None = None,
        series_id: str | None = None,
        asset_cat: str | None = None,
        issuer_cat: str | None = None,
        inv_country: str | None = None,
        min_val_usd: float | str | None = None,
        is_restricted_sec: bool | None = None,
        fair_val_level: int | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        period: str | None = None,
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
                isin=isin,
                lei=lei,
                name=name,
                registrant_cik=registrant_cik,
                filing_id=filing_id,
                series_id=series_id,
                asset_cat=asset_cat,
                issuer_cat=issuer_cat,
                inv_country=inv_country,
                min_val_usd=min_val_usd,
                is_restricted_sec=is_restricted_sec,
                fair_val_level=fair_val_level,
                period_start=period_start,
                period_end=period_end,
                period=period,
                limit=limit,
                offset=offset,
                sort=sort,
                order=order,
            ),
        )

    def iter_holdings(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate holdings across pages. Same filters as holdings()."""
        return self._iter_offset(f"{PATH}/holdings", filters)

    def entities(self, **kwargs: Any) -> dict[str, Any]:
        """Registrant rollup. Accepts limit, offset, search, sort, order."""
        return self._entities(f"{PATH}/entities", **kwargs)
