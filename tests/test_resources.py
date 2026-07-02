import httpx
import pytest


def make_echo_client(make_client, seen):
    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"data": []})

    return make_client(handler)


def test_paths(make_client):
    seen = []
    client = make_echo_client(make_client, seen)

    client.health()
    client.health_ready()
    client.entities.get("320193")
    client.coverage.by_issuer("AAPL")
    client.coverage.by_family()
    client.coverage.intake(period="daily")
    client.coverage.data_as_of()
    client.insiders.get("cik_accession")
    client.insiders.owners("1234")
    client.insiders.biography("1234")
    client.insiders.buy_sell_ratio(ticker="AAPL")
    client.insiders.entities(search="apple")
    client.institutional_holdings.holdings(cusip="037833100")
    client.money_market_funds.series_nav(series_id="S000001")
    client.registration_statements.get_section("some-uuid")

    paths = [r.url.path for r in seen]
    assert paths == [
        "/v1/health",
        "/v1/health/ready",
        "/v1/entities/320193",
        "/v1/coverage/by-issuer/AAPL",
        "/v1/coverage/by-family",
        "/v1/intake",
        "/v1/data-as-of",
        "/v1/insiders/cik_accession",
        "/v1/insiders/owners/1234",
        "/v1/insiders/biography/1234",
        "/v1/insiders/buy-sell-ratio",
        "/v1/insiders/entities",
        "/v1/institutional-holdings/holdings",
        "/v1/money-market-funds/series-nav",
        "/v1/registration-statements/sections/some-uuid",
    ]


def test_series_rejects_unknown_filter(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    with pytest.raises(TypeError):
        client.money_market_funds.class_nav(bogus="x")


def test_get_with_include_form_data(make_client):
    seen = []
    client = make_echo_client(make_client, seen)
    client.private_offerings.get("fid", include_form_data=False)
    assert seen[0].url.params["include_form_data"] == "false"
