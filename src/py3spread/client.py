from __future__ import annotations

import os
import random
import time
from typing import Any

import httpx

from ._version import __version__
from .exceptions import APIConnectionError, error_from_response
from .resources import (
    BeneficialOwnership,
    Changes,
    Coverage,
    Entities,
    Filings,
    FundCensus,
    FundPortfolios,
    Insiders,
    InstitutionalHoldings,
    MoneyMarketFunds,
    PrivateOfferings,
    ProposedSales,
    ProxyVotes,
    RegAOfferings,
    RegistrationStatements,
)

DEFAULT_BASE_URL = "https://api.3spread.com"
ENV_API_KEY = "THREESPREAD_API_KEY"

_RETRY_STATUSES = frozenset({429, 502, 503})
_TICKER_PARAMS = frozenset({"ticker", "issuer_ticker"})


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any]:
    if not params:
        return {}
    out = {}
    for key, value in params.items():
        if value is None:
            continue
        # the api rejects lowercase tickers instead of normalizing them
        if key in _TICKER_PARAMS and isinstance(value, str):
            value = value.upper()
        out[key] = value
    return out


class Client:
    """Client for the 3spread API.

    Reads the API key from the THREESPREAD_API_KEY environment variable
    if not passed explicitly. Get a key at https://3spread.com/auth/signup.

    Each filing family is an attribute (`filings`, `insiders`,
    `institutional_holdings`, `beneficial_ownership`, ...) carrying that
    family's list/iter/get methods.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        transport: httpx.BaseTransport | None = None,
    ):
        api_key = api_key or os.environ.get(ENV_API_KEY)
        if not api_key:
            raise ValueError(
                "no API key given; pass api_key= or set the "
                f"{ENV_API_KEY} environment variable"
            )
        self.max_retries = max_retries
        self._http = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            transport=transport,
            headers={
                "apikey": api_key,
                "user-agent": f"py3spread/{__version__}",
            },
        )

        self.filings = Filings(self)
        self.insiders = Insiders(self)
        self.institutional_holdings = InstitutionalHoldings(self)
        self.private_offerings = PrivateOfferings(self)
        self.fund_portfolios = FundPortfolios(self)
        self.beneficial_ownership = BeneficialOwnership(self)
        self.proposed_sales = ProposedSales(self)
        self.fund_census = FundCensus(self)
        self.money_market_funds = MoneyMarketFunds(self)
        self.proxy_votes = ProxyVotes(self)
        self.reg_a_offerings = RegAOfferings(self)
        self.registration_statements = RegistrationStatements(self)
        self.entities = Entities(self)
        self.coverage = Coverage(self)
        self.changes = Changes(self)

    def request(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """GET a path and return the parsed JSON body, retrying 429/502/503."""
        params = _clean_params(params)
        for attempt in range(self.max_retries + 1):
            try:
                resp = self._http.get(path, params=params)
            except httpx.TransportError as exc:
                if attempt >= self.max_retries:
                    raise APIConnectionError(str(exc)) from exc
                time.sleep(self._backoff(attempt))
                continue
            if resp.status_code in _RETRY_STATUSES and attempt < self.max_retries:
                time.sleep(self._backoff(attempt, resp.headers.get("retry-after")))
                continue
            if resp.is_success:
                return resp.json()
            try:
                body = resp.json()
            except ValueError:
                body = {"message": resp.text}
            raise error_from_response(resp.status_code, body, resp.headers)
        raise AssertionError("unreachable")

    def _backoff(self, attempt: int, retry_after: str | None = None) -> float:
        if retry_after:
            try:
                return max(0.0, float(retry_after))
            except ValueError:
                pass
        return min(30.0, 0.5 * 2**attempt) + random.uniform(0, 0.1)

    def health(self) -> dict[str, Any]:
        """Service health, including per-family data_as_of freshness."""
        return self.request("/v1/health")

    def health_ready(self) -> dict[str, Any]:
        """Readiness probe."""
        return self.request("/v1/health/ready")

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()
