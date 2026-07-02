from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/insiders"


class Insiders(Resource):
    """Forms 3, 4, 5: insider beneficial ownership filings."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        issuer_cik: str | None = None,
        form_type: str | None = None,
        is_amendment: bool | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        role: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of insider filings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                issuer_cik=issuer_cik,
                form_type=form_type,
                is_amendment=is_amendment,
                period_start=period_start,
                period_end=period_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                role=role,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate insider filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str) -> dict[str, Any]:
        """Full detail for one filing, with all reporting owners and transactions."""
        return self._get(f"{PATH}/{filing_id}")

    def transactions(
        self,
        *,
        transaction_kind: str | None = None,
        issuer_cik: str | None = None,
        issuer_ticker: str | None = None,
        rpt_owner_cik: str | None = None,
        transaction_code: str | None = None,
        transaction_acquired_disposed_code: str | None = None,
        transaction_start: str | None = None,
        transaction_end: str | None = None,
        min_value: float | str | None = None,
        max_value: float | str | None = None,
        role: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """One page of the cross-filing transaction stream.

        Requires an identity filter (issuer_cik, issuer_ticker, or
        rpt_owner_cik) plus transaction_start and/or transaction_end.
        A single bound gives a 1-day window; both bounds allow up to 730 days.
        """
        return self._get(
            f"{PATH}/transactions",
            dict(
                transaction_kind=transaction_kind,
                issuer_cik=issuer_cik,
                issuer_ticker=issuer_ticker,
                rpt_owner_cik=rpt_owner_cik,
                transaction_code=transaction_code,
                transaction_acquired_disposed_code=transaction_acquired_disposed_code,
                transaction_start=transaction_start,
                transaction_end=transaction_end,
                min_value=min_value,
                max_value=max_value,
                role=role,
                limit=limit,
                offset=offset,
            ),
        )

    def iter_transactions(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate transactions across pages. Same filters as transactions()."""
        return self._iter_offset(f"{PATH}/transactions", filters)

    def owners(
        self,
        rpt_owner_cik: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """Filings by one reporting owner."""
        return self._get(
            f"{PATH}/owners/{rpt_owner_cik}",
            dict(limit=limit, offset=offset, sort=sort, order=order),
        )

    def biography(self, rpt_owner_cik: str) -> dict[str, Any]:
        """Reporting-owner biography."""
        return self._get(f"{PATH}/biography/{rpt_owner_cik}")

    def buy_sell_ratio(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        sic: str | None = None,
        window_days: int | None = None,
    ) -> dict[str, Any]:
        """Buy/sell ratio over a trailing window."""
        return self._get(
            f"{PATH}/buy-sell-ratio",
            dict(cik=cik, ticker=ticker, sic=sic, window_days=window_days),
        )

    def entities(self, **kwargs: Any) -> dict[str, Any]:
        """Issuer rollup. Accepts limit, offset, search, sort, order."""
        return self._entities(f"{PATH}/entities", **kwargs)
