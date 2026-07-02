from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/money-market-funds"


class MoneyMarketFunds(Resource):
    """Form N-MFP2: money market fund monthly portfolio reports."""

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        registrant_cik: str | None = None,
        series_id: str | None = None,
        money_market_fund_category: str | None = None,
        is_final_filing: bool | None = None,
        feeder_fund_flag: bool | None = None,
        master_fund_flag: bool | None = None,
        retail_money_market_fund_flag: bool | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of N-MFP2 filings. Needs an identity filter or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                registrant_cik=registrant_cik,
                series_id=series_id,
                money_market_fund_category=money_market_fund_category,
                is_final_filing=is_final_filing,
                feeder_fund_flag=feeder_fund_flag,
                master_fund_flag=master_fund_flag,
                retail_money_market_fund_flag=retail_money_market_fund_flag,
                period_start=period_start,
                period_end=period_end,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate N-MFP2 filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str, *, include_form_data: bool | None = None) -> dict[str, Any]:
        """Full detail for one N-MFP2 filing."""
        return self._get(f"{PATH}/{filing_id}", dict(include_form_data=include_form_data))

    def securities(
        self,
        *,
        cusip_member: str | None = None,
        isin_id: str | None = None,
        lei_id: str | None = None,
        name_of_issuer: str | None = None,
        registrant_cik: str | None = None,
        filing_id: str | None = None,
        investment_category: str | None = None,
        security_eligibility_flag: str | None = None,
        daily_liquid_asset_security_flag: bool | None = None,
        weekly_liquid_asset_security_flag: bool | None = None,
        illiquid_security_flag: bool | None = None,
        min_value: float | str | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort: str | None = None,
        order: str | None = None,
    ) -> dict[str, Any]:
        """One page of the cross-filing securities stream."""
        return self._get(
            f"{PATH}/securities",
            dict(
                cusip_member=cusip_member,
                isin_id=isin_id,
                lei_id=lei_id,
                name_of_issuer=name_of_issuer,
                registrant_cik=registrant_cik,
                filing_id=filing_id,
                investment_category=investment_category,
                security_eligibility_flag=security_eligibility_flag,
                daily_liquid_asset_security_flag=daily_liquid_asset_security_flag,
                weekly_liquid_asset_security_flag=weekly_liquid_asset_security_flag,
                illiquid_security_flag=illiquid_security_flag,
                min_value=min_value,
                period_start=period_start,
                period_end=period_end,
                limit=limit,
                offset=offset,
                sort=sort,
                order=order,
            ),
        )

    def iter_securities(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate securities across pages. Same filters as securities()."""
        return self._iter_offset(f"{PATH}/securities", filters)

    def series_nav(self, **kwargs: Any) -> dict[str, Any]:
        """Series-level NAV series. Accepts registrant_cik, series_id, filing_id,
        date_start, date_end, granularity, limit, offset, sort, order."""
        return self._series(f"{PATH}/series-nav", kwargs)

    def liquid_assets(self, **kwargs: Any) -> dict[str, Any]:
        """Series-level liquid-assets series. Same filters as series_nav()."""
        return self._series(f"{PATH}/liquid-assets", kwargs)

    def class_nav(self, **kwargs: Any) -> dict[str, Any]:
        """Class-level NAV series. Same filters as series_nav() plus classes_id."""
        return self._series(f"{PATH}/class-nav", kwargs)

    def class_flows(self, **kwargs: Any) -> dict[str, Any]:
        """Class-level subscriptions/redemptions series. Same filters as class_nav()."""
        return self._series(f"{PATH}/class-flows", kwargs)

    def entities(self, **kwargs: Any) -> dict[str, Any]:
        """Registrant rollup. Accepts limit, offset, search, sort, order."""
        return self._entities(f"{PATH}/entities", **kwargs)

    _SERIES_PARAMS = frozenset(
        {
            "registrant_cik",
            "series_id",
            "classes_id",
            "filing_id",
            "date_start",
            "date_end",
            "granularity",
            "limit",
            "offset",
            "sort",
            "order",
        }
    )

    def _series(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        unknown = set(params) - self._SERIES_PARAMS
        if unknown:
            raise TypeError(f"unexpected filters: {sorted(unknown)}")
        return self._get(path, params)
