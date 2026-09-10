from __future__ import annotations

from typing import Any, Iterator

from ._base import Resource

PATH = "/v1/financials"


class Financials(Resource):
    """Financial statements, metrics, ratios, and quant factors from 10-K/10-Q filings.

    This family is not part of the ``FAMILIES`` changefeed enum — it has its
    own discovery and detail endpoints rather than fitting the filing-family
    list/iter/get pattern.  ``version`` is required on the series endpoints
    (``statements``, ``metrics``, ``ratios``, ``factors``): pass ``"latest"``,
    ``"original"``, or ``"as_of:YYYY-MM-DD"``.
    """

    # ------------------------------------------------------------------ #
    # filings
    # ------------------------------------------------------------------ #

    def list(
        self,
        *,
        cik: str | None = None,
        ticker: str | None = None,
        form_type: str | None = None,
        fiscal_year: int | None = None,
        is_valid: bool | None = None,
        accepted_start: str | None = None,
        accepted_end: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of validated 10-K / 10-Q filings. Needs cik/ticker or a bounded window."""
        return self._get(
            PATH,
            dict(
                cik=cik,
                ticker=ticker,
                form_type=form_type,
                fiscal_year=fiscal_year,
                is_valid=is_valid,
                accepted_start=accepted_start,
                accepted_end=accepted_end,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate financials filings across pages. Same filters as list()."""
        return self._iter_cursor(PATH, filters)

    def get(self, filing_id: str) -> dict[str, Any]:
        """The filing plus every block it reported, including comparative columns."""
        return self._get(f"{PATH}/{filing_id}")

    # ------------------------------------------------------------------ #
    # statements
    # ------------------------------------------------------------------ #

    def statements(
        self,
        *,
        version: str,
        cik: str | None = None,
        ticker: str | None = None,
        statement_type: str | None = None,
        fiscal_year: int | None = None,
        fiscal_quarter: int | None = None,
        period_length: int | None = None,
        fiscal_year_start: int | None = None,
        fiscal_year_end: int | None = None,
        is_valid: bool | None = None,
        derived: bool | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of validated statement blocks (bs / inc / cf).

        ``version`` is required: ``"latest"``, ``"original"``, or
        ``"as_of:YYYY-MM-DD"``.
        """
        return self._get(
            f"{PATH}/statements",
            dict(
                cik=cik,
                ticker=ticker,
                version=version,
                statement_type=statement_type,
                fiscal_year=fiscal_year,
                fiscal_quarter=fiscal_quarter,
                period_length=period_length,
                fiscal_year_start=fiscal_year_start,
                fiscal_year_end=fiscal_year_end,
                is_valid=is_valid,
                derived=derived,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter_statements(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate statement blocks across pages. Same filters as statements()."""
        return self._iter_cursor(f"{PATH}/statements", filters)

    def get_statement(self, block_id: str) -> dict[str, Any]:
        """Point read of a single statement block by UUID."""
        return self._get(f"{PATH}/statements/{block_id}")

    # ------------------------------------------------------------------ #
    # metrics
    # ------------------------------------------------------------------ #

    def metrics(
        self,
        *,
        version: str,
        cik: str | None = None,
        ticker: str | None = None,
        category: str | None = None,
        statement_type: str | None = None,
        currency: str | None = None,
        fiscal_year: int | None = None,
        fiscal_quarter: int | None = None,
        period_length: int | None = None,
        fiscal_year_start: int | None = None,
        fiscal_year_end: int | None = None,
        min_value: float | str | None = None,
        max_value: float | str | None = None,
        is_valid: bool | None = None,
        derived: bool | None = None,
        sort: str | None = None,
        order: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of canonical line-item metrics as a time-series.

        Requires cik or ticker. ``version`` is required.
        """
        return self._get(
            f"{PATH}/metrics",
            dict(
                cik=cik,
                ticker=ticker,
                version=version,
                category=category,
                statement_type=statement_type,
                currency=currency,
                fiscal_year=fiscal_year,
                fiscal_quarter=fiscal_quarter,
                period_length=period_length,
                fiscal_year_start=fiscal_year_start,
                fiscal_year_end=fiscal_year_end,
                min_value=min_value,
                max_value=max_value,
                is_valid=is_valid,
                derived=derived,
                sort=sort,
                order=order,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter_metrics(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate metrics across pages. Same filters as metrics()."""
        return self._iter_cursor(f"{PATH}/metrics", filters)

    # ------------------------------------------------------------------ #
    # ratios
    # ------------------------------------------------------------------ #

    def ratios(
        self,
        *,
        version: str,
        cik: str | None = None,
        ticker: str | None = None,
        ratio_name: str | None = None,
        ratio_category: str | None = None,
        spine: str | None = None,
        fiscal_year: int | None = None,
        fiscal_quarter: int | None = None,
        period_length: int | None = None,
        fiscal_year_start: int | None = None,
        fiscal_year_end: int | None = None,
        min_value: float | str | None = None,
        max_value: float | str | None = None,
        include_low_materiality: bool | None = None,
        derived: bool | None = None,
        sort: str | None = None,
        order: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of precomputed ratio time-series.

        Requires cik or ticker. ``version`` is required.
        """
        return self._get(
            f"{PATH}/ratios",
            dict(
                cik=cik,
                ticker=ticker,
                version=version,
                ratio_name=ratio_name,
                ratio_category=ratio_category,
                spine=spine,
                fiscal_year=fiscal_year,
                fiscal_quarter=fiscal_quarter,
                period_length=period_length,
                fiscal_year_start=fiscal_year_start,
                fiscal_year_end=fiscal_year_end,
                min_value=min_value,
                max_value=max_value,
                include_low_materiality=include_low_materiality,
                derived=derived,
                sort=sort,
                order=order,
                limit=limit,
                cursor=cursor,
            ),
        )

    def iter_ratios(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate ratios across pages. Same filters as ratios()."""
        return self._iter_cursor(f"{PATH}/ratios", filters)

    def ratio_names(self) -> dict[str, Any]:
        """The canonical ratio_name vocabulary (31 taxonomy-defined keys)."""
        return self._get(f"{PATH}/ratios/names")

    # ------------------------------------------------------------------ #
    # factors
    # ------------------------------------------------------------------ #

    def factors(
        self,
        *,
        version: str,
        cik: str | None = None,
        ticker: str | None = None,
        factor_name: str | None = None,
        period_type: str | None = None,
        spine: str | None = None,
        fiscal_year: int | None = None,
        fiscal_year_start: int | None = None,
        fiscal_year_end: int | None = None,
        period_end: str | None = None,
        value_min: float | str | None = None,
        value_max: float | str | None = None,
        pctile_min: float | str | None = None,
        pctile_max: float | str | None = None,
        sort: str | None = None,
        order: str | None = None,
        limit: int | None = None,
        latest_only: bool | None = None,
        cursor: str | None = None,
    ) -> dict[str, Any]:
        """One page of the quant factor library (90 factors).

        Two modes: per-entity series (pass cik/ticker) or cross-company screen
        (omit identity, pass factor_name + period). ``version`` is required.
        """
        return self._get(
            f"{PATH}/factors",
            dict(
                cik=cik,
                ticker=ticker,
                version=version,
                factor_name=factor_name,
                period_type=period_type,
                spine=spine,
                fiscal_year=fiscal_year,
                fiscal_year_start=fiscal_year_start,
                fiscal_year_end=fiscal_year_end,
                period_end=period_end,
                value_min=value_min,
                value_max=value_max,
                pctile_min=pctile_min,
                pctile_max=pctile_max,
                sort=sort,
                order=order,
                limit=limit,
                latest_only=latest_only,
                cursor=cursor,
            ),
        )

    def iter_factors(self, **filters: Any) -> Iterator[dict[str, Any]]:
        """Iterate factors across pages. Same filters as factors()."""
        return self._iter_cursor(f"{PATH}/factors", filters)

    def factor_names(self) -> dict[str, Any]:
        """The 90-key factor vocabulary."""
        return self._get(f"{PATH}/factors/names")

    def factor_percentile(
        self,
        *,
        factor_name: str,
        period_end: str,
        as_of: str,
        cik: str | None = None,
        ticker: str | None = None,
        period_type: str | None = None,
    ) -> dict[str, Any]:
        """Dynamic point-in-time percentile rank for one factor / period / as-of date.

        ``factor_name``, ``period_end``, and ``as_of`` are required.
        """
        return self._get(
            f"{PATH}/factors/percentile",
            dict(
                cik=cik,
                ticker=ticker,
                factor_name=factor_name,
                period_type=period_type,
                period_end=period_end,
                as_of=as_of,
            ),
        )

    # ------------------------------------------------------------------ #
    # categories
    # ------------------------------------------------------------------ #

    def categories(self) -> dict[str, Any]:
        """The canonical metric category vocabulary (177 taxonomy-defined keys)."""
        return self._get(f"{PATH}/categories")
