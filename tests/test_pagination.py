import httpx


def test_cursor_iteration(make_client):
    pages = [
        {"data": [{"filing_id": "a"}, {"filing_id": "b"}], "has_more": True, "next_cursor": "CUR1"},
        {"data": [{"filing_id": "c"}], "has_more": False, "next_cursor": None},
    ]
    urls = []

    def handler(request):
        urls.append(str(request.url))
        return httpx.Response(200, json=pages[len(urls) - 1])

    client = make_client(handler)
    rows = list(client.filings.iter(ticker="AAPL"))
    assert [r["filing_id"] for r in rows] == ["a", "b", "c"]
    assert len(urls) == 2
    # cursor added on page two, original filter kept
    assert "cursor" not in urls[0]
    assert "cursor=CUR1" in urls[1]
    assert "ticker=AAPL" in urls[1]


def test_offset_iteration_has_more_shape(make_client):
    pages = [
        {"data": [{"id": 1}, {"id": 2}], "has_more": True, "page": 1, "page_size": 2},
        {"data": [{"id": 3}], "has_more": False, "page": 2, "page_size": 2},
    ]
    urls = []

    def handler(request):
        urls.append(str(request.url))
        return httpx.Response(200, json=pages[len(urls) - 1])

    client = make_client(handler)
    rows = list(client.insiders.iter_transactions(issuer_ticker="AAPL"))
    assert [r["id"] for r in rows] == [1, 2, 3]
    assert "offset=0" in urls[0]
    assert "offset=2" in urls[1]


def test_offset_iteration_total_shape(make_client):
    pages = [
        {"data": [{"id": 1}, {"id": 2}], "total": 3, "page": 1, "page_size": 2, "total_pages": 2},
        {"data": [{"id": 3}], "total": 3, "page": 2, "page_size": 2, "total_pages": 2},
    ]
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(200, json=pages[calls["n"] - 1])

    client = make_client(handler)
    rows = list(client.registration_statements.iter(ticker="AAPL"))
    assert [r["id"] for r in rows] == [1, 2, 3]
    assert calls["n"] == 2


def test_offset_iteration_stops_on_empty_page(make_client):
    def handler(request):
        return httpx.Response(200, json={"data": [], "page": 1, "page_size": 50})

    client = make_client(handler)
    assert list(client.fund_portfolios.iter(registrant_cik="123")) == []


def test_changes_iter_uses_family_path(make_client):
    urls = []

    def handler(request):
        urls.append(str(request.url))
        return httpx.Response(200, json={"data": [{"filing_id": "x"}], "next_cursor": None})

    client = make_client(handler)
    rows = list(client.changes.iter("insiders", since="2026-01-01T00:00:00"))
    assert rows == [{"filing_id": "x"}]
    assert "/v1/changes/insiders" in urls[0]
    assert "since=" in urls[0]
