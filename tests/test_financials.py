import httpx
import pytest

from py3spread import Client


def make_echo_client(make_client, seen):
    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"data": []})

    return make_client(handler)


# ------------------------------------------------------------------ #
# list / iter
# ------------------------------------------------------------------ #


def test_list_forwards_params(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.list(
        ticker="AAPL",
        form_type="10-K",
        fiscal_year=2024,
        is_valid=True,
        accepted_start="2024-01-01",
        accepted_end="2024-12-31",
        limit=50,
        cursor="abc",
    )
    params = seen[0].url.params
    assert params["ticker"] == "AAPL"
    assert params["form_type"] == "10-K"
    assert params["fiscal_year"] == "2024"
    assert params["is_valid"] == "true"
    assert params["accepted_start"] == "2024-01-01"
    assert params["accepted_end"] == "2024-12-31"
    assert params["limit"] == "50"
    assert params["cursor"] == "abc"


def test_list_omits_unset_params(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.list(ticker="AAPL")
    params = seen[0].url.params
    assert "cik" not in params
    assert "form_type" not in params
    assert "fiscal_year" not in params


def test_get_filing(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.get("0000320193_0000320193-24-000001")
    assert seen[0].url.path == "/v1/financials/0000320193_0000320193-24-000001"


# ------------------------------------------------------------------ #
# statements
# ------------------------------------------------------------------ #


def test_statements_requires_version(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.statements(version="latest", ticker="AAPL")
    params = seen[0].url.params
    assert params["version"] == "latest"
    assert params["ticker"] == "AAPL"


def test_statements_forwards_all_params(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.statements(
        version="as_of:2024-06-30",
        cik="320193",
        statement_type="bs",
        fiscal_year=2024,
        fiscal_quarter=4,
        period_length=12,
        fiscal_year_start=2020,
        fiscal_year_end=2024,
        is_valid=True,
        derived=False,
        limit=5,
        cursor="cur",
    )
    params = seen[0].url.params
    assert params["version"] == "as_of:2024-06-30"
    assert params["cik"] == "320193"
    assert params["statement_type"] == "bs"
    assert params["fiscal_year"] == "2024"
    assert params["fiscal_quarter"] == "4"
    assert params["period_length"] == "12"
    assert params["fiscal_year_start"] == "2020"
    assert params["fiscal_year_end"] == "2024"
    assert params["is_valid"] == "true"
    assert params["derived"] == "false"
    assert params["limit"] == "5"
    assert params["cursor"] == "cur"


def test_get_statement(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.get_statement("550e8400-e29b-41d4-a716-446655440000")
    assert seen[0].url.path == "/v1/financials/statements/550e8400-e29b-41d4-a716-446655440000"


# ------------------------------------------------------------------ #
# metrics
# ------------------------------------------------------------------ #


def test_metrics_forwards_params(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.metrics(
        version="latest",
        cik="320193",
        category="total_revenue",
        statement_type="inc",
        currency="USD",
        fiscal_year=2024,
        fiscal_quarter=4,
        period_length=12,
        fiscal_year_start=2020,
        fiscal_year_end=2024,
        min_value="1000000",
        max_value="500000000000",
        is_valid=True,
        derived=False,
        sort="value",
        order="desc",
        limit=100,
        cursor="c",
    )
    params = seen[0].url.params
    assert params["version"] == "latest"
    assert params["cik"] == "320193"
    assert params["category"] == "total_revenue"
    assert params["statement_type"] == "inc"
    assert params["currency"] == "USD"
    assert params["fiscal_year"] == "2024"
    assert params["fiscal_quarter"] == "4"
    assert params["period_length"] == "12"
    assert params["fiscal_year_start"] == "2020"
    assert params["fiscal_year_end"] == "2024"
    assert params["min_value"] == "1000000"
    assert params["max_value"] == "500000000000"
    assert params["is_valid"] == "true"
    assert params["derived"] == "false"
    assert params["sort"] == "value"
    assert params["order"] == "desc"
    assert params["limit"] == "100"
    assert params["cursor"] == "c"


# ------------------------------------------------------------------ #
# ratios
# ------------------------------------------------------------------ #


def test_ratios_forwards_params(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.ratios(
        version="original",
        ticker="AAPL",
        ratio_name="roe_pct",
        ratio_category="profitability",
        spine="commercial_industrial",
        fiscal_year=2024,
        fiscal_quarter=4,
        period_length=12,
        fiscal_year_start=2020,
        fiscal_year_end=2024,
        min_value="10",
        max_value="50",
        include_low_materiality=True,
        derived=False,
        sort="value",
        order="desc",
        limit=100,
        cursor="c",
    )
    params = seen[0].url.params
    assert params["version"] == "original"
    assert params["ticker"] == "AAPL"
    assert params["ratio_name"] == "roe_pct"
    assert params["ratio_category"] == "profitability"
    assert params["spine"] == "commercial_industrial"
    assert params["fiscal_year"] == "2024"
    assert params["fiscal_quarter"] == "4"
    assert params["period_length"] == "12"
    assert params["fiscal_year_start"] == "2020"
    assert params["fiscal_year_end"] == "2024"
    assert params["min_value"] == "10"
    assert params["max_value"] == "50"
    assert params["include_low_materiality"] == "true"
    assert params["derived"] == "false"
    assert params["sort"] == "value"
    assert params["order"] == "desc"
    assert params["limit"] == "100"
    assert params["cursor"] == "c"


def test_ratio_names(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.ratio_names()
    assert seen[0].url.path == "/v1/financials/ratios/names"


# ------------------------------------------------------------------ #
# factors
# ------------------------------------------------------------------ #


def test_factors_per_entity_mode(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.factors(
        version="latest",
        cik="320193",
        factor_name="roe",
        period_type="FY",
        spine="commercial_industrial",
        fiscal_year=2024,
        fiscal_year_start=2020,
        fiscal_year_end=2024,
        period_end="2024-09-28",
        value_min="0.1",
        value_max="0.5",
        pctile_min="50",
        pctile_max="100",
        sort="value",
        order="desc",
        limit=100,
        latest_only=True,
        cursor="c",
    )
    params = seen[0].url.params
    assert params["version"] == "latest"
    assert params["cik"] == "320193"
    assert params["factor_name"] == "roe"
    assert params["period_type"] == "FY"
    assert params["spine"] == "commercial_industrial"
    assert params["fiscal_year"] == "2024"
    assert params["fiscal_year_start"] == "2020"
    assert params["fiscal_year_end"] == "2024"
    assert params["period_end"] == "2024-09-28"
    assert params["value_min"] == "0.1"
    assert params["value_max"] == "0.5"
    assert params["pctile_min"] == "50"
    assert params["pctile_max"] == "100"
    assert params["sort"] == "value"
    assert params["order"] == "desc"
    assert params["limit"] == "100"
    assert params["latest_only"] == "true"
    assert params["cursor"] == "c"


def test_factors_cross_company_screen(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    # no cik/ticker — cross-company screen mode
    client.financials.factors(
        version="latest",
        factor_name="roe",
        period_type="FY",
        period_end="2024-09-28",
    )
    params = seen[0].url.params
    assert "cik" not in params
    assert "ticker" not in params
    assert params["factor_name"] == "roe"
    assert params["period_type"] == "FY"
    assert params["period_end"] == "2024-09-28"


def test_factor_names(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.factor_names()
    assert seen[0].url.path == "/v1/financials/factors/names"


def test_factor_percentile(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.factor_percentile(
        cik="320193",
        factor_name="roe",
        period_type="FY",
        period_end="2024-09-28",
        as_of="2024-12-31",
    )
    params = seen[0].url.params
    assert seen[0].url.path == "/v1/financials/factors/percentile"
    assert params["cik"] == "320193"
    assert params["factor_name"] == "roe"
    assert params["period_type"] == "FY"
    assert params["period_end"] == "2024-09-28"
    assert params["as_of"] == "2024-12-31"


def test_factor_percentile_omits_unset(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.factor_percentile(
        ticker="AAPL",
        factor_name="roe",
        period_end="2024-09-28",
        as_of="2024-12-31",
    )
    params = seen[0].url.params
    assert "cik" not in params
    assert "period_type" not in params
    assert params["ticker"] == "AAPL"


# ------------------------------------------------------------------ #
# categories
# ------------------------------------------------------------------ #


def test_categories(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.financials.categories()
    assert seen[0].url.path == "/v1/financials/categories"


# ------------------------------------------------------------------ #
# cursor iteration
# ------------------------------------------------------------------ #


def test_statements_iter_cursor(make_client):
    pages = [
        {"data": [{"block_id": "a"}], "next_cursor": "CUR1"},
        {"data": [{"block_id": "b"}], "next_cursor": None},
    ]
    urls = []

    def handler(request):
        urls.append(str(request.url))
        return httpx.Response(200, json=pages[len(urls) - 1])

    client = make_client(handler)
    rows = list(client.financials.iter_statements(version="latest", cik="320193"))
    assert [r["block_id"] for r in rows] == ["a", "b"]
    assert "cursor" not in urls[0]
    assert "cursor=CUR1" in urls[1]
    assert "version=latest" in urls[1]


def test_metrics_iter_cursor(make_client):
    pages = [
        {"data": [{"category": "revenue"}], "next_cursor": "X"},
        {"data": [{"category": "income"}], "next_cursor": None},
    ]
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(200, json=pages[calls["n"] - 1])

    client = make_client(handler)
    rows = list(client.financials.iter_metrics(version="original", ticker="AAPL"))
    assert [r["category"] for r in rows] == ["revenue", "income"]
    assert calls["n"] == 2


def test_ratios_iter_cursor(make_client):
    pages = [
        {"data": [{"ratio_name": "roe_pct"}], "next_cursor": "Y"},
        {"data": [{"ratio_name": "roa_pct"}], "next_cursor": None},
    ]
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(200, json=pages[calls["n"] - 1])

    client = make_client(handler)
    rows = list(client.financials.iter_ratios(version="latest", cik="320193"))
    assert [r["ratio_name"] for r in rows] == ["roe_pct", "roa_pct"]
    assert calls["n"] == 2


def test_factors_iter_cursor(make_client):
    pages = [
        {"data": [{"factor_name": "roe"}], "next_cursor": "Z"},
        {"data": [{"factor_name": "roa"}], "next_cursor": None},
    ]
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(200, json=pages[calls["n"] - 1])

    client = make_client(handler)
    rows = list(client.financials.iter_factors(version="latest", cik="320193"))
    assert [r["factor_name"] for r in rows] == ["roe", "roa"]
    assert calls["n"] == 2


def test_filings_iter_cursor(make_client):
    pages = [
        {"data": [{"filing_id": "a"}], "next_cursor": "C1"},
        {"data": [{"filing_id": "b"}], "next_cursor": None},
    ]
    urls = []

    def handler(request):
        urls.append(str(request.url))
        return httpx.Response(200, json=pages[len(urls) - 1])

    client = make_client(handler)
    rows = list(client.financials.iter(ticker="AAPL"))
    assert [r["filing_id"] for r in rows] == ["a", "b"]
    assert "cursor=C1" in urls[1]
    assert "ticker=AAPL" in urls[1]
